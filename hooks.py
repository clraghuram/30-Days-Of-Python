"""
MkDocs hook to copy images into docs/images at build time.

This avoids committing a duplicate of the images/ directory.
The markdown files reference /images/... which works because
we temporarily make the files available under docs/images/.
"""

import os
import shutil

def on_pre_build(config):
    """Copy root images/ into docs/images/ before each build."""
    src_dir = "images"
    docs_dir = config.get("docs_dir", "docs")
    dst_dir = os.path.join(docs_dir, "images")

    if not os.path.isdir(src_dir):
        return

    # Ensure clean state
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    os.makedirs(dst_dir)

    for name in os.listdir(src_dir):
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir, name)
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        except Exception:
            pass


def on_post_build(config):
    """Clean up the temporary docs/images/ after build."""
    docs_dir = config.get("docs_dir", "docs")
    dst_dir = os.path.join(docs_dir, "images")
    if os.path.exists(dst_dir):
        try:
            shutil.rmtree(dst_dir)
        except Exception:
            pass
