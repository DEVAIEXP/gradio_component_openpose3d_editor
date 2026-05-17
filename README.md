# `gradio-openpose-3d`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.3%20-%20blue">  
<a href="https://huggingface.co/spaces/elismasilva/gradio_openpose3d_editor"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Demo-blue"></a>  
<span>💻 <a href='https://github.com/DEVAIEXP/gradio_component_openpose3d_editor'>Component GitHub Code</a></span>

A powerful, custom interactive 3D character posing component for Gradio apps using `gr.HTML` and Three.js (r160). It allows users to manipulate a 3D model's bones in real-time, adjust camera angles, apply aspect ratio cropping, and export the resulting pose map directly to the Python backend.

Perfect for AI image generation pipelines (like ControlNet or T2I-Adapter), reference posing, or any Gradio app requiring precise visual spatial conditioning.

Inspired by the Openart OpenPose Editor

## Features and Key Characteristics

- **Interactive 3D Viewport:** Full OrbitControls implementation (zoom, pan, rotate) and TransformControls for bone manipulation.
- **Client-Side Rendering via ESM:** Loads modern Three.js directly via CDN (`esm.sh`) dynamically. No heavy local Node.js builds required.
- **Built-in Undo/Redo System:** Autonomous history tracking for bone transformations (Rotation and Translation) with keyboard shortcuts (`Ctrl+Z`, `Ctrl+Shift+Z`).
- **Aspect Ratio Cropping:** Visual crop overlay with predefined aspect ratios (1:1, 16:9, 9:16, etc.) to frame the exact pose you need.
- **Direct Python Export:** clicking the export icon renders the cropped canvas and sends it directly to Gradio server as a PNG file path.
- **Theme Aware UI:** The floating toolbar completely integrates with Gradio's native light/dark mode CSS variables.

## Installation

```bash
pip install gradio-openpose3d-editor
```

## Usage

```py
import gradio as gr
from gradio_openpose3d_editor import OpenPose3DEditor

def process_pose(image_path: str):
    """
    Receives the PNG file path exported by the 3D editor.
    You can open it with PIL, pass it to ControlNet, etc.
    """
    if not image_path:
        return None
    return image_path

with gr.Blocks() as demo:
    gr.Markdown("# 🧍 3D OpenPose Editor")
    
    with gr.Row():
        # Initialize the 3D Editor
        editor = OpenPose3DEditor(
            #fbx_url="https://huggingface.co/buckets/elismasilva/assets/resolve/base.fbx?download=true",  here optional if you want a custom fbx model.
            height=560
        )
        
        # Output component to display the exported PNG
        preview = gr.Image(label="Exported Pose Map", type="filepath")
    
    # Listen to the 'export' event triggered by the floppy disk icon inside the component
    editor.export(
        fn=process_pose,
        inputs=editor,
        outputs=preview
    )
    
demo.launch()
```

## Component API

### Initialization Properties

| Property | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `fbx_url` | `str` | *Default URL* | Optional URL or relative path to the `.fbx` character model. |
| `height` | `int` | `540` | Height of the 3D viewport container in pixels. |
| `label` | `str \| None` | `None` | Optional label for the component. |
| `visible` | `bool` | `True` | Whether the component is visible on the screen. |
| `elem_id` | `str \| None` | `None` | Custom HTML ID for targeting with CSS or JavaScript. |
| `elem_classes` | `list[str] \| str \| None` | `None` | Additional CSS classes applied to the component wrapper. |

### Events

| Event | Description |
| :--- | :--- |
| `.export(fn, inputs, outputs, ...)` | Triggered when the user clicks the "Floppy Disk" export button in the UI. The component's `value` is automatically updated to the server-side file path (`str`) of the rendered PNG image, which is then passed to your Python function. |


## Acknowledgements / Credits

The default 3D model used in this component is provided under the CC BY 4.0 license:
* ["Base Mesh T Pose FBX"](https://skfb.ly/owXpQ) by [nuffylabz](https://sketchfab.com/nuffylabz) is licensed under [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/).