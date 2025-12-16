from inkex import EffectExtension, Image, Rectangle, ClipPath, errormsg
from PIL import Image as PILImage


class ClipBg(EffectExtension):
    def effect(self):
        # 1. Validate Selection
        if not self.svg.selection:
            errormsg("Please select an image first.")
            return

        # Iterate through selection (handling multiple images if selected)
        for node in self.svg.selection.filter(Image):
            self.process_image(node)

    def process_image(self, node):
        # 2. Extract Image Data
        # Inkscape images may be linked (href path) or embedded (base64)
        xlink = node.get("xlink:href") or node.get("href")

        try:
            if xlink.startswith("data:"):
                # Handle Embedded Image
                from io import BytesIO
                from base64 import b64decode

                head, data = xlink.split(",", 1)
                image_bytes = b64decode(data)
                pil_img = PILImage.open(BytesIO(image_bytes))
            else:
                # Handle Linked Image (resolve absolute path)
                image_path = node.style.get("abs_path", xlink)
                # If path is relative, make it absolute based on svg file location
                if not image_path.startswith("/") and self.options.input_file:
                    from os.path import dirname, join

                    base_dir = dirname(self.options.input_file)
                    image_path = join(base_dir, image_path)

                pil_img = PILImage.open(image_path)
        except Exception as e:
            errormsg(f"Could not load image data: {str(e)}")
            return

        # 3. Calculate Bounding Box (Autocrop)
        # getbbox() returns (left, upper, right, lower) of non-zero alpha pixels
        bbox = pil_img.getbbox()

        if not bbox:
            errormsg("Image is fully transparent or empty.")
            return

        # 4. Map Pixels to SVG Units
        # We must scale pixel coordinates to the SVG image dimensions
        px_left, px_top, px_right, px_bottom = bbox

        img_pixel_w, img_pixel_h = pil_img.size

        # node.width/height are the dimensions in SVG units
        # We need to parse them to floats (they might have units like 'mm')
        svg_w = node.width
        svg_h = node.height

        # Calculate scale factors
        scale_x = svg_w / img_pixel_w
        scale_y = svg_h / img_pixel_h

        # Calculate clipping rectangle in SVG coordinates relative to image position
        # Note: We add node.left/top because clipPath uses userSpaceOnUse by default
        clip_x = node.left + (px_left * scale_x)
        clip_y = node.top + (px_top * scale_y)
        clip_w = (px_right - px_left) * scale_x
        clip_h = (px_bottom - px_top) * scale_y

        # 5. Create SVG Elements
        # Create unique ID for the clip path
        clip_id = self.svg.get_unique_id("clipbg")

        # Define the ClipPath container
        clip_path = ClipPath()
        clip_path.set("id", clip_id)

        # Define the Rectangle
        rect = Rectangle()
        rect.set("x", clip_x)
        rect.set("y", clip_y)
        rect.set("width", clip_w)
        rect.set("height", clip_h)

        clip_path.append(rect)

        # Add ClipPath to Defs (create Defs if missing)
        defs = self.svg.defs
        defs.append(clip_path)

        # 6. Apply to Image
        node.set("clip-path", f"url(#{clip_id})")


if __name__ == "__main__":
    ClipBg().run()
