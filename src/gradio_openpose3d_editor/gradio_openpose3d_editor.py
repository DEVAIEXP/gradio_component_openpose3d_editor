"""
OpenPose3D — Gradio 6 Custom Component based on gr.HTML
Encapsulates a 3D pose editor using Three.js (r160) via ESM.
"""

import gradio as gr

_HTML_TEMPLATE = """
<div id="op3d-root" style="position:relative;width:100%;height:${height}px;overflow:hidden;border-radius:var(--block-radius, 10px);background:var(--background-fill-primary, #e8e8e8);">
  <!-- Three.js canvas mount point -->
  <div id="op3d-mount" style="width:100%;height:100%;"></div>

  <!-- CROP OVERLAY -->
  <div id="op3d-crop-overlay" style="
    position:absolute;top:0;left:0;width:100%;height:100%;
    pointer-events:none;display:flex;align-items:center;
    justify-content:center;z-index:10;">
    <div id="op3d-crop-box" style="border:2px solid rgba(255,255,255,0.85);
      box-shadow:0 0 0 9999px rgba(0,0,0,0.38);
      transition:width .25s ease,height .25s ease;"></div>
  </div>

  <!-- VERTICAL TOOLBAR (Right aligned, Theme Aware) -->
  <div id="op3d-toolbar" style="
    position:absolute;top:50%;right:16px;transform:translateY(-50%);
    display:flex;flex-direction:column;align-items:center;gap:6px;
    background:var(--block-background-fill);
    border:1px solid var(--border-color-primary);
    padding:12px 8px;border-radius:12px;
    box-shadow:var(--shadow-drop);
    z-index:20;">

    <!-- Aspect ratio -->
    <select id="op3d-aspect" title="Aspect Ratio" style="
      padding:6px 2px;border-radius:6px;border:1px solid var(--border-color-primary);
      background:var(--background-fill-secondary);color:var(--body-text-color);
      font-size:11px;font-weight:600;cursor:pointer;outline:none;
      text-align:center;width:44px;appearance:none;-webkit-appearance:none;text-align-last:center;">
      <option value="1:1">1:1</option>
      <option value="16:9">16:9</option>
      <option value="4:3">4:3</option>
      <option value="3:2">3:2</option>
      <option value="5:4">5:4</option>
      <option value="2:3">2:3</option>
      <option value="4:5">4:5</option>
      <option value="9:16">9:16</option>
    </select>

    <div class="op3d-sep"></div>

    <!-- Rotate Button -->
    <button id="op3d-btn-rotate" class="op3d-icon-btn active" title="Rotate">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21.5 2v6h-6"/>
        <path d="M21.34 15.57a10 10 0 1 1-.57-8.38"/>
      </svg>
    </button>

    <!-- Move Button -->
    <button id="op3d-btn-translate" class="op3d-icon-btn" title="Move">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2l-3 4h2.5v4.5H7V8L3 11l4 3v-2.5h4.5V16H9l3 4 3-4h-2.5v-4.5H17V14l4-3-4-3v2.5h-4.5V6H15z"/>
      </svg>
    </button>

    <div class="op3d-sep"></div>

    <!-- Undo Button -->
    <button id="op3d-btn-undo" class="op3d-icon-btn" title="Undo (Ctrl+Z)" disabled>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 14 4 9 9 4"/><path d="M20 20v-7a4 4 0 0 0-4-4H4"/>
      </svg>
    </button>

    <!-- Redo Button -->
    <button id="op3d-btn-redo" class="op3d-icon-btn" title="Redo (Ctrl+Shift+Z)" disabled>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 14 20 9 15 4"/><path d="M4 20v-7a4 4 0 0 1 4-4h12"/>
      </svg>
    </button>

    <div class="op3d-sep"></div>

    <!-- Reset Button -->
    <button id="op3d-btn-reset" class="op3d-icon-btn" title="Reset Pose (Ctrl+R)">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>
      </svg>
    </button>

    <div class="op3d-sep"></div>

    <!-- Export Button (Floppy disk) -->
    <button id="op3d-btn-export" class="op3d-icon-btn export" title="Export to Python">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="2" width="20" height="20" rx="2" ry="2"/>
        <path d="M7 2v7h10V2"/>
        <rect x="9" y="2" width="4" height="5" rx="0"/>
        <rect x="6" y="14" width="12" height="7" rx="1"/>
      </svg>
    </button>
  </div>
</div>
"""

_CSS_TEMPLATE = """
  .op3d-icon-btn {
    display: flex; align-items: center; justify-content: center;
    width: 38px; height: 38px;
    border: none; border-radius: 8px;
    background: transparent; color: var(--body-text-color);
    cursor: pointer; transition: all 0.15s ease;
  }
  .op3d-icon-btn:hover { background: var(--background-fill-secondary); }
  .op3d-icon-btn.active { background: var(--color-accent); color: white; }
  
  .op3d-icon-btn:disabled { opacity: 0.3 !important; cursor: default; }
  .op3d-icon-btn:disabled:hover { background: transparent; }
  
  .op3d-icon-btn.export { color: var(--color-accent); }
  .op3d-icon-btn.export:hover { background: var(--color-accent); color: white; }

  .op3d-sep { width: 24px; height: 1px; background: var(--border-color-primary); margin: 2px 0; }
"""

_JS_ON_LOAD = r"""
(async () => {
  try {
    // Dynamic ESM Imports
    const THREE = await import('https://esm.sh/three@0.160.0');
    const { OrbitControls } = await import('https://esm.sh/three@0.160.0/examples/jsm/controls/OrbitControls.js');
    const { TransformControls } = await import('https://esm.sh/three@0.160.0/examples/jsm/controls/TransformControls.js');
    const { FBXLoader } = await import('https://esm.sh/three@0.160.0/examples/jsm/loaders/FBXLoader.js');

    const root = element.querySelector('#op3d-mount');
    if (!root) return;

    const fbxUrl = props.fbx_url || './base.fbx';

    // ==================== SCENE ====================
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xe8e8e8); 

    const W = () => root.clientWidth;
    const H = () => root.clientHeight;

    // ==================== CAMERA ====================
    const camera = new THREE.PerspectiveCamera(60, W() / H(), 0.1, 1000);
    camera.position.set(80, 60, 70);
    camera.lookAt(0, 30, 0);

    // ==================== RENDERER ====================
    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setSize(W(), H());
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.outputColorSpace = THREE.SRGBColorSpace; 
    renderer.domElement.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;';
    root.appendChild(renderer.domElement);

    // ==================== ORBIT CONTROLS ====================
    const orbit = new OrbitControls(camera, renderer.domElement);
    orbit.target.set(0, 30, 0);
    orbit.minDistance = 20; 
    orbit.maxDistance = 500;
    orbit.minPolarAngle = Math.PI / 6; 
    orbit.maxPolarAngle = 0.7 * Math.PI;
    orbit.enableDamping = true; 
    orbit.dampingFactor = 0.05;
    orbit.update();

    // ==================== LIGHTS ====================
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x447392, 3);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 3); 
    dirLight.position.set(0, 200, 0); 
    dirLight.castShadow = true; 
    scene.add(dirLight);

    const dirLight2 = new THREE.DirectionalLight(0xffffff, 3); 
    dirLight2.position.set(0, 200, 100); 
    scene.add(dirLight2);

    // ==================== GRID & FLOOR ====================
    const gridHelper = new THREE.GridHelper(2000, 20, 0x000000, 0x000000);
    gridHelper.material.opacity = 0.2; 
    gridHelper.material.transparent = true;
    scene.add(gridHelper);

    const floorGeo = new THREE.PlaneGeometry(2000, 2000);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x787878, roughness: 0.2, metalness: 0 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2; 
    floor.receiveShadow = true;
    scene.add(floor);

    // ==================== TRANSFORM CONTROLS ====================
    const transformControl = new TransformControls(camera, renderer.domElement);
    transformControl.setMode('rotate'); 
    transformControl.setSpace('local');
    scene.add(transformControl);
    
    transformControl.addEventListener('dragging-changed', event => { 
        orbit.enabled = !event.value; 
    });

    // ==================== STATE VARIABLES ====================
    let characterMesh = null, currentMode = 'rotate';
    const proxyMeshes = [], boneMap = new Map();
    let initialPoseSnapshot = null;
    const history = [], redoStack = [], MAX_HISTORY = 50;

    // ==================== COLORS ====================
    function getBoneColor(boneName) {
      const name = boneName.toLowerCase();
      if (name.includes('head') || name.includes('neck')) return 0x0000ff;
      if (name.includes('spine')) return 0x004080;
      if (name.includes('hips'))  return 0x8000ff;
      if (name.includes('shoulder')) return 0x8A0000;
      if (name.includes('rightarm') || name.includes('leftarm')) return 0xF99D36;
      if (name.includes('rightforearm') || name.includes('leftforearm')) return 0xFFFF00;
      if (name.includes('hand')) return 0x00aaff;
      if (name.includes('upleg') || name.includes('leg') || name.includes('knee')) {
          return name.includes('left') ? 0x00ff88 : 0xff0088;
      }
      if (name.includes('rightfoot')) return 0xff0088;
      if (name.includes('leftfoot'))  return 0x00ff88;
      return 0x44ffaa;
    }

    function makeCircleTexture(color, selected = false) {
      const size = 128;
      const canvas = document.createElement('canvas');
      canvas.width = size;
      canvas.height = size;
      const ctx = canvas.getContext('2d');
      
      const hex = '#' + color.toString(16).padStart(6, '0');
      
      ctx.beginPath(); 
      ctx.arc(size / 2, size / 2, size / 2 - 3, 0, Math.PI * 2);
      ctx.fillStyle = hex; 
      ctx.fill();
      
      ctx.strokeStyle = selected ? 'rgba(255,255,255,1)' : 'rgba(255,255,255,0.5)';
      ctx.lineWidth = selected ? 10 : 4; 
      ctx.stroke();
      
      return new THREE.CanvasTexture(canvas);
    }

    // ==================== POSE SNAPSHOTS ====================
    function capturePose() {
      const snapshot = {};
      boneMap.forEach((_, bone) => { 
        snapshot[bone.uuid] = {
            quaternion: bone.quaternion.clone(),
            position: bone.position.clone()
        }; 
      });
      return snapshot;
    }

    function applySnapshot(snapshot) {
      boneMap.forEach((_, bone) => { 
        if(snapshot[bone.uuid]){
            bone.quaternion.copy(snapshot[bone.uuid].quaternion);
            bone.position.copy(snapshot[bone.uuid].position);
        } 
      });
    }
    
    function captureInitialPose() { 
        initialPoseSnapshot = capturePose(); 
    }

    function pushHistory() {
      history.push(capturePose());
      if(history.length > MAX_HISTORY) history.shift();
      redoStack.length = 0; 
      updateUndoRedoBtns();
    }
    
    function undo() { 
        if(history.length === 0) return; 
        redoStack.push(capturePose()); 
        applySnapshot(history.pop()); 
        updateUndoRedoBtns(); 
    }
    
    function redo() { 
        if(redoStack.length === 0) return; 
        history.push(capturePose()); 
        applySnapshot(redoStack.pop()); 
        updateUndoRedoBtns(); 
    }

    function updateUndoRedoBtns() {
      element.querySelector('#op3d-btn-undo').disabled = history.length === 0;
      element.querySelector('#op3d-btn-redo').disabled = redoStack.length === 0;
    }

    transformControl.addEventListener('mouseDown', () => pushHistory());

    // ==================== FBX LOADING ====================
    function findMainBones(model) {
      const ignored = ['finger', 'thumb', 'index', 'middle', 'ring', 'pinky', 'toe', '_end', 'rigneck'];
      const wanted  = ['hips', 'spine', 'head', 'shoulder', 'arm', 'forearm', 'hand', 'upleg', 'leg', 'foot'];
      const result  = [];
      model.traverse(child => {
        if(!child.isBone) return;
        const n = child.name.toLowerCase();
        if(ignored.some(k => n.includes(k))) return;
        if(wanted.some(k => n.includes(k))) result.push(child);
      });
      return result;
    }

    function createControlPoints(bones) {
      bones.forEach(bone => {
        const color = getBoneColor(bone.name);
        const texture = makeCircleTexture(color);
        const mat = new THREE.SpriteMaterial({ map: texture, depthTest: false, transparent: true, opacity: 0.95 });
        
        const sprite = new THREE.Sprite(mat);
        sprite.scale.set(10, 10, 1);
        sprite.userData = { bone, type: 'controlPoint', region: bone.name, baseColor: color };
        
        scene.add(sprite); 
        proxyMeshes.push(sprite); 
        boneMap.set(bone, sprite);
      });
    }

    function fitCameraToModel() {
      if(!characterMesh) return;
      const box = new THREE.Box3().setFromObject(characterMesh);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      const maxDim = Math.max(size.x, size.y, size.z);
      
      const distance = maxDim * 1.8;
      camera.position.set(
          center.x + distance * 0,
          center.y + distance * 0.5,
          center.z + distance * 1.0
      );
      camera.lookAt(center); 
      orbit.target.copy(center); 
      orbit.update();
    }

    function selectProxy(proxy) {
      const bone = proxy.userData.bone;
      transformControl.detach(); 
      transformControl.attach(bone); 
      transformControl.setMode(currentMode);
      
      proxyMeshes.forEach(p => { 
          p.material.opacity = 0.95;
          p.material.map = makeCircleTexture(p.userData.baseColor); 
          p.material.needsUpdate = true; 
      });
      proxy.material.map = makeCircleTexture(proxy.userData.baseColor, true); 
      proxy.material.needsUpdate = true;
    }

    function selectRootBone() {
      if(proxyMeshes.length === 0) return;
      const hip = proxyMeshes.find(p => p.userData.region.toLowerCase().includes('hips'));
      selectProxy(hip || proxyMeshes[0]);
    }

    const loader = new FBXLoader();
    loader.load(fbxUrl, obj => {
      characterMesh = obj;
      const box = new THREE.Box3().setFromObject(characterMesh);
      const size = box.getSize(new THREE.Vector3());
      const center = box.getCenter(new THREE.Vector3());
      
      characterMesh.position.set(-center.x, -box.min.y, -center.z);
      
      const targetHeight = 100;
      const scale = targetHeight / size.y;
      characterMesh.scale.setScalar(scale);

      const mainBones = findMainBones(characterMesh);
      createControlPoints(mainBones);

      characterMesh.traverse(child => {
        if(child.isMesh){
          child.castShadow = true; 
          child.receiveShadow = true;
        }
      });
      
      scene.add(characterMesh);
      characterMesh.updateMatrixWorld(true);
      captureInitialPose();
      
      fitCameraToModel(); 
      selectRootBone();
    }, undefined, err => console.error('FBX load error:', err));

    // ==================== RAYCASTER ====================
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    
    renderer.domElement.addEventListener('pointerdown', event => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      
      raycaster.setFromCamera(mouse, camera);
      const visible = proxyMeshes.filter(p => p.visible);
      const hits = raycaster.intersectObjects(visible, false);
      
      if(hits.length > 0) {
          selectProxy(hits[0].object);
      } else if(!transformControl.dragging) {
        transformControl.detach();
        proxyMeshes.forEach(p => { 
            p.material.map = makeCircleTexture(p.userData.baseColor); 
            p.material.needsUpdate = true; 
        });
      }
    });

    // ==================== CROP BOX ====================
    const cropBox = element.querySelector('#op3d-crop-box');
    
    function updateCropBox(ratioString) {
      const [w, h] = ratioString.split(':').map(Number);
      
      // Calculate taking into account the UI space
      const maxH = root.clientHeight * 0.85; 
      const maxW = root.clientWidth * 0.85;
      
      let boxH = Math.min(maxH, 520);
      let boxW = (boxH * w) / h;
      
      if(boxW > maxW){
          boxW = maxW; 
          boxH = (boxW * h) / w;
      }
      
      cropBox.style.width = `${boxW}px`; 
      cropBox.style.height = `${boxH}px`;
    }
    
    const aspectSel = element.querySelector('#op3d-aspect');
    aspectSel.addEventListener('change', e => updateCropBox(e.target.value));
    updateCropBox('1:1');

    // ==================== UI EVENTS ====================
    element.querySelector('#op3d-btn-rotate').addEventListener('click', () => {
      currentMode = 'rotate'; 
      transformControl.setMode('rotate'); 
      transformControl.setSpace('local');
      proxyMeshes.forEach(p => { p.visible = true; });
      
      element.querySelector('#op3d-btn-rotate').classList.add('active');
      element.querySelector('#op3d-btn-translate').classList.remove('active');
    });

    element.querySelector('#op3d-btn-translate').addEventListener('click', () => {
      currentMode = 'translate'; 
      transformControl.setMode('translate'); 
      transformControl.setSpace('world');
      proxyMeshes.forEach(p => { p.visible = p.userData.region.toLowerCase().includes('hips'); });
      selectRootBone();
      
      element.querySelector('#op3d-btn-translate').classList.add('active');
      element.querySelector('#op3d-btn-rotate').classList.remove('active');
    });

    element.querySelector('#op3d-btn-undo').addEventListener('click', undo);
    element.querySelector('#op3d-btn-redo').addEventListener('click', redo);

    element.querySelector('#op3d-btn-reset').addEventListener('click', () => {
      if(!characterMesh || !initialPoseSnapshot) return;
      pushHistory(); 
      applySnapshot(initialPoseSnapshot);
    });

    // ==================== EXPORT TO PYTHON ====================
    element.querySelector('#op3d-btn-export').addEventListener('click', async () => {
      if(!characterMesh) return;
      
      proxyMeshes.forEach(p => { p.visible = false; });
      transformControl.visible = false; 
      floor.visible = false; 
      gridHelper.visible = false;
      
      renderer.render(scene, camera);

      const rect = cropBox.getBoundingClientRect();
      const canvasRect = renderer.domElement.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      
      const srcX = Math.round((rect.left - canvasRect.left) * dpr);
      const srcY = Math.round((rect.top - canvasRect.top) * dpr);
      const srcW = Math.round(rect.width * dpr);
      const srcH = Math.round(rect.height * dpr);

      const cv = document.createElement('canvas'); 
      cv.width = srcW; 
      cv.height = srcH;
      
      const ctx = cv.getContext('2d');
      ctx.drawImage(
          renderer.domElement,
          srcX, srcY, srcW, srcH,
          0,    0,    srcW, srcH
      );

      proxyMeshes.forEach(p => { p.visible = true; });
      transformControl.visible = true; 
      floor.visible = true; 
      gridHelper.visible = true;

      const blob = await new Promise(res => cv.toBlob(res, 'image/png'));
      const file = new File([blob], 'openpose.png', { type: 'image/png' });
      try {
        const { path } = await upload(file);
        props.value = path;        
        trigger('export');         
      } catch(e) {
        console.error('Upload error:', e);
      }
    });

    // Keyboard Shortcuts
    window.addEventListener('keydown', e => {
      if(e.ctrlKey || e.metaKey){
        if(e.key === 'z' && !e.shiftKey) { e.preventDefault(); undo(); }
        if(e.key === 'z' && e.shiftKey)  { e.preventDefault(); redo(); }
        if(e.key === 'y')                { e.preventDefault(); redo(); }
        if(e.key === 'r')                { e.preventDefault(); element.querySelector('#op3d-btn-reset').click(); }
      }
    });

    // ==================== ANIMATION LOOP ====================
    function animate() {
      requestAnimationFrame(animate);
      if(characterMesh) {
        characterMesh.updateMatrixWorld(true);
        for(const [bone, sprite] of boneMap.entries()){
          const wp = new THREE.Vector3(); 
          bone.getWorldPosition(wp); 
          sprite.position.copy(wp);
          const d = camera.position.distanceTo(wp); 
          sprite.scale.set(d * 0.018, d * 0.018, 1);
        }
      }
      orbit.update(); 
      renderer.render(scene, camera);
    }
    animate();

    // ==================== RESIZE OBSERVER ====================
    const ro = new ResizeObserver(() => {
      camera.aspect = W() / H(); 
      camera.updateProjectionMatrix();
      renderer.setSize(W(), H());
      updateCropBox(aspectSel.value);
    });
    ro.observe(root);

  } catch (error) {
    console.error("Failed to initialize 3D editor:", error);
  }
})();
"""

class OpenPose3DEditor(gr.HTML):
    """
    3D Body Pose Editor based on Three.js (r160).

    Parameters
    ----------
    fbx_url : str
        URL or relative path to the FBX model to load.
    height : int
        Component height in pixels (default 540).

    Events
    -------
    .export(fn, outputs=...)
        Triggered when the user clicks the save (floppy disk) button.
        The component's `value` is updated to the generated PNG file path 
        on the Gradio server, ready to be used in Image, File, etc.
    """

    def __init__(self, fbx_url: str = "https://huggingface.co/buckets/elismasilva/assets/resolve/base.fbx?download=true", height: int = 540, **kwargs):
        super().__init__(
            value=None,
            fbx_url=fbx_url,
            height=height,
            html_template=_HTML_TEMPLATE,
            css_template=_CSS_TEMPLATE,
            js_on_load=_JS_ON_LOAD,
            apply_default_css=False,
            **kwargs,
        )

    def api_info(self):
        # The exported value is the server-side PNG file path
        return {"type": "string", "description": "Server-side path of the exported PNG"}