# 全栈机器人仿真项目：从零到一的Web控制指南

## 简介

本教程旨在为初学者提供一个从零开始、详尽无遗的指南，带领您从安装一个纯净的Ubuntu系统开始，一步步掌握Linux基本操作、安装ROS 2和Gazebo，并最终成功部署一个可以通过Web浏览器进行实时交互控制的UR5e机械臂仿真项目。

本教程的最终目标是实现：

-   一个在**Gazebo**中运行的UR5e机械臂仿真环境。
-   一个可以通过**网页**上的滑块来控制机械臂运动的前端界面。
-   前端界面能够**实时同步**仿真环境中机械臂的姿态。

这个项目将带您穿越从底层机器人操作系统到上层Web开发的完整技术栈，是提升个人工程实践能力的绝佳项目。

---

## 第一章：基础环境准备 (Ubuntu 22.04)

### 1.1 安装Ubuntu 22.04 LTS

对于机器人开发，一个稳定、纯净的Linux环境至关重要。我们推荐使用Ubuntu 22.04 LTS (长期支持版)，因为它与我们项目所需的核心软件ROS 2 Humble Hawksbill完全兼容。

-   **下载Ubuntu镜像**: 前往 [Ubuntu官方网站](https://ubuntu.com/download/desktop) 下载 "Ubuntu 22.04.x LTS" 的ISO镜像文件。
-   **制作启动盘**:
    -   准备一个容量至少为8GB的U盘。
    -   使用 [Rufus](https://rufus.ie/zh_CN/) (Windows) 或 [balenaEtcher](https://www.balena.io/etcher/) (Windows/macOS/Linux) 等工具，将下载的ISO镜像文件写入U盘，制作成系统启动盘。
-   **安装系统**:
    1.  将制作好的U盘插入您的电脑。
    2.  重启电脑，并进入BIOS/UEFI设置（通常是开机时按`F2`, `F12`, `DEL`或`ESC`键），将U盘设置为第一启动项。
    3.  保存设置并退出，电脑将从U盘启动，进入Ubuntu安装界面。
    4.  按照图形化界面的提示进行安装。建议选择“**最小安装**”以保持系统纯净，并勾选“**为图形或无线硬件，以及MP3和其他媒体格式安装第三方软件**”选项，以确保驱动程序正常。
    5.  在分区时，如果您是单系统，可以选择“**清除整个磁盘并安装Ubuntu**”；如果您需要双系统，请务必谨慎操作，选择“**其他选项**”手动分区。

### 1.2 Linux终端入门

终端是Linux环境下的核心工具。按下 `Ctrl+Alt+T` 可以快速打开一个终端窗口。
你也可以綁定快捷鍵

**1.2.1 系统更新**

安装完系统后，第一件事就是更新软件包列表和已安装的软件。
sudu相當於就是ubuntu系統裏面的應用商城

```bash
sudo apt update      # 更新可用的软件包列表
sudo apt upgrade -y  # 升级所有已安装的软件包，-y表示自动确认
```

**1.2.2 核心命令入门**

-   `ls`: 列出当前目录下的文件和文件夹。
    -   `ls -l`: 显示详细信息。
    -   `ls -a`: 显示包括隐藏文件在内的所有文件。
    -   `ls -R`: 显示文件夾下的所有文件夾下的文件。

-   `cd`: 切换目录。
    -   `cd ~`: 回到主目录 (Home)。
    -   `cd ..`: 回到上一级目录。
    -   `cd /`: 回到根目录。
-   `pwd`: 显示当前所在的目录路径。
-   `mkdir <目录名>`: 创建一个新的目录。
-   `touch <文件名>`: 创建一个空文件。
-   `cp <源文件> <目标位置>`: 复制文件或目录。
    -   `cp -r <源目录> <目标位置>`: 递归复制整个目录。
-   `mv <源文件> <目标位置>`: 移动或重命名文件/目录。
-   `rm <文件名>`: 删除文件。
    -   `rm -r <目录名>`: 递归删除整个目录（**此操作非常危险，请谨慎使用！**）。
-   `sudo <命令>`: 以超级用户（管理员）权限执行命令。

**1.2.3 安装常用工具**

```bash
# 安装Git版本控制工具
sudo apt install git -y

# 安装文本编辑器(推荐)和网络工具
sudo apt install vim curl wget -y

# 安装Python3和包管理工具pip
sudo apt install python3 python3-pip -y
```

---

## 第二章：机器人核心软件安装

### 2.1 安装ROS 2 Humble Hawksbill

ROS (Robot Operating System) 是机器人开发的标准框架。我们将安装与Ubuntu 22.04对应的`Humble`版本。

1.  **设置区域设置 (Locale)**: 确保您的系统支持UTF-8。
    ```bash
    sudo apt install locales -y
    sudo locale-gen en_US en_US.UTF-8
    sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
    export LANG=en_US.UTF-8
    ```
2.  **添加ROS 2软件源**:
    ```bash
    sudo apt install software-properties-common -y
    sudo add-apt-repository universe -y
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
    ```
3.  **安装ROS 2桌面完整版**:
    ```bash
    sudo apt update
    sudo apt install ros-humble-desktop-full -y
    ```
4.  **安装ROS 2开发工具**:
    ```bash
    sudo apt install ros-dev-tools -y
    ```
5.  **设置环境**:
    将ROS 2的环境设置脚本添加到您的 `.bashrc` 文件中，这样每次打开新终端时都会自动加载ROS环境。
    ```bash
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
    source ~/.bashrc
    ```
6.  **验证安装**: 打开一个**新**终端，运行 `ros2` 命令。如果看到很多可用的子命令，说明ROS 2已成功安装。

### 2.2 安装Gazebo仿真器

我们安装的`ros-humble-desktop-full`已经自带了Gazebo，但为了确保所有与ROS集成的部分都已安装，可以运行以下命令：
```bash
sudo apt install ros-humble-gazebo-* -y
```
验证安装：在终端输入 `gazebo`，如果Gazebo的图形界面能成功打开，说明安装无误。

---

## 第三章：项目部署与后端启动

### 3.1 创建ROS 2工作区并获取源码

1.  **创建工作区目录**:
    ```bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws/src
    ```
2.  **克隆项目仓库**: 我们将克隆Universal Robots官方提供的ROS 2仿真包。
    ```bash
    git clone https://github.com/UniversalRobots/Universal_Robots_ROS2_Gazebo_Simulation.git -b humble
    ```
3.  **安装依赖**:
    回到工作区根目录，使用`rosdep`工具自动安装所有缺失的依赖项。
    ```bash
    cd ~/ros2_ws
    rosdep init  # 如果是第一次使用，需要初始化
    rosdep update
    rosdep install --from-paths src -y --ignore-src
    ```
4.  **构建工作区**:
    ```bash
    colcon build --symlink-install
    ```
    构建完成后，工作区目录下会新增 `build`, `install`, `log` 三个目录。

### 3.2 启动Gazebo仿真环境

每次启动仿真前，都需要先加载工作区的环境。

1.  **打开一个新终端 (终端1)**。
2.  **Source工作区环境**:
    ```bash
    cd ~/ros2_ws
    source ./install/setup.bash
    ```
    **提示**: 你可以把这行命令也加入到 `~/.bashrc` 中，这样就不用每次手动执行了。
3.  **启动UR5e仿真**:
    ```bash
    ros2 launch ur_simulation_gazebo ur_sim_control.launch.py ur_type:=ur5e
    ```
    稍等片刻，你应该能看到Gazebo窗口打开，并且里面有一个UR5e机械臂。至此，我们的后端仿真环境已经成功运行！

### 3.3 启动通信桥梁 (rosbridge)

为了让Web前端能与ROS 2后端通信，我们需要一个WebSocket桥梁。

1.  **安装rosbridge**:
    ```bash
    sudo apt install ros-humble-rosbridge-server -y
    ```
2.  **启动rosbridge**:
    -   **打开一个新终端 (终端2)**。
    -   **Source ROS 2环境**: `source /opt/ros/humble/setup.bash`
    -   **启动服务**:
        ```bash
        ros2 launch rosbridge_server rosbridge_websocket_launch.xml
        ```
    当看到 `Rosbridge WebSocket server started on port 9090` 的信息时，说明通信桥梁已成功架设。

---

## 第四章：前端界面开发与全栈联调

### 4.1 创建前端项目

1.  **创建项目目录**:
    ```bash
    mkdir ~/ur_web_control
    cd ~/ur_web_control
    ```
2.  **创建核心文件**:
    ```bash
    touch index.html main.js
    ```
3.  **准备机器人模型文件**:
    Web前端需要加载机器人的URDF模型和3D网格文件(meshes)。
    -   **打开一个新终端**，并source ROS 2环境 (`source /opt/ros/humble/setup.bash`)。
    -   **生成URDF文件**:
        ```bash
        ros2 run xacro xacro $(ros2 pkg prefix ur_description)/share/ur_description/urdf/ur.urdf.xacro ur_type:=ur5e > ~/ur_web_control/urdf/ur5e.urdf
        ```
    -   **复制3D模型**:
        ```bash
        cp -r $(ros2 pkg prefix ur_description)/share/ur_description/meshes ~/ur_web_control/urdf/
        ```
4.  **下载前端依赖库**:
    为了稳定和避免网络问题，我们将所有JavaScript库下载到本地。
    ```bash
    mkdir js
    cd js
    curl -L -o three.module.js https://unpkg.com/three@0.165.0/build/three.module.js
    curl -L -o OrbitControls.js https://unpkg.com/three@0.165.0/examples/jsm/controls/OrbitControls.js
    curl -L -o STLLoader.js https://unpkg.com/three@0.165.0/examples/jsm/loaders/STLLoader.js
    ```

### 4.2 编写前端代码

将以下代码内容分别复制到对应的文件中。

#### `index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>UR Robot Web Control (Final Verified Version)</title>
    <style>
        body { font-family: sans-serif; margin: 0; }
        #viewer { width: 100vw; height: 100vh; display: block; }
        #controls-panel { position: absolute; top: 10px; left: 10px; background: rgba(255,255,255,0.8); padding: 15px; border-radius: 5px; max-width: 500px; }
        .joint-slider { margin: 10px 0; display: flex; align-items: center; }
        label { display: inline-block; width: 160px; font-size: 14px; }
        input[type=range] { flex-grow: 1; }
        #connection-status { margin-bottom: 10px; font-weight: bold; }
        h1 { font-size: 24px; margin-top: 0; }
    </style>
</head>
<body>
    <div id="viewer"></div>
    <div id="controls-panel">
        <h1>UR Web Controller</h1>
        <div id="connection-status" style="color: red;">正在断开...</div>
        <div class="controls">
            <h3>关节控制</h3>
            <div class="joint-slider"><label>shoulder_pan_joint:</label><input type="range" id="q1" min="-3.14" max="3.14" step="0.01" value="0"></div>
            <div class="joint-slider"><label>shoulder_lift_joint:</label><input type="range" id="q2" min="-3.14" max="3.14" step="0.01" value="-1.57"></div>
            <div class="joint-slider"><label>elbow_joint:</label><input type="range" id="q3" min="-3.14" max="3.14" step="0.01" value="0"></div>
            <div class="joint-slider"><label>wrist_1_joint:</label><input type="range" id="q4" min="-3.14" max="3.14" step="0.01" value="-1.57"></div>
            <div class="joint-slider"><label>wrist_2_joint:</label><input type="range" id="q5" min="-3.14" max="3.14" step="0.01" value="0"></div>
            <div class="joint-slider"><label>wrist_3_joint:</label><input type="range" id="q6" min="-3.14" max="3.14" step="0.01" value="0"></div>
            <button id="send-goal-btn">发送目标</button>
        </div>
    </div>

    <!-- 加载ROS Web通信库 -->
    <script src="https://cdn.jsdelivr.net/npm/roslib@1/build/roslib.min.js"></script>

    <!-- 使用importmap管理本地JS模块 -->
    <script type="importmap">
      {
        "imports": {
          "three": "./js/three.module.js",
          "three/addons/": "./js/"
        }
      }
    </script>

    <!-- 加载主逻辑脚本 -->
    <script type="module" src="main.js"></script>
</body>
</html>
```

#### `main.js`
```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/OrbitControls.js';
import { STLLoader } from 'three/addons/STLLoader.js';

// =================================================================================================
// BEGIN: 内置的、兼容的 URDFLoader 代码
// =================================================================================================
const {
	Loader,
	Matrix4,
	Mesh,
	MeshPhongMaterial,
	Vector3,
} = THREE;

class URDFLoader extends Loader {
	constructor( manager ) {
		super( manager );
		this.packages = {};
		this.loadMeshCb = this.defaultLoadMesh.bind( this );
	}
	load( url, onLoad, onProgress, onError ) {
		const scope = this;
		const loader = new THREE.FileLoader( scope.manager );
		loader.setPath( scope.path );
		loader.setResponseType( 'text' );
		loader.load( url, text => {
			try {
				onLoad( scope.parse( text ) );
			} catch ( e ) {
				if ( onError ) { onError( e ); } 
                else { console.error( e ); }
				scope.manager.itemError( url );
			}
		}, onProgress, onError );
	}
	parse( text ) {
		const parser = new DOMParser();
		const urdf = parser.parseFromString( text, 'text/xml' );
        if (urdf.getElementsByTagName('parsererror').length > 0) {
            throw new Error('URDFLoader: Failed to parse XML. Is the URDF file valid?');
        }
		const robot = urdf.children[ 0 ];
		const links = {};
		const joints = {};
		for ( const child of robot.children ) {
			const type = child.nodeName.toLowerCase();
			if ( type === 'link' ) {
				const name = child.getAttribute( 'name' );
				links[ name ] = this.parseLink( child );
			} else if ( type === 'joint' ) {
				const name = child.getAttribute( 'name' );
				joints[ name ] = this.parseJoint( child );
			}
		}
        const jointMap = {};
        for (const name in joints) {
            const joint = joints[name];
            jointMap[joint.child] = joint;
        }

        const rootLinks = Object.keys(links).filter(name => !jointMap[name]);
        if (rootLinks.length === 0) {
             throw new Error('URDFLoader: Could not find root link. No link is not a child of any joint.');
        }
        if (rootLinks.length > 1) {
             throw new Error(`URDFLoader: Found multiple root links: ${rootLinks.join(', ')}`);
        }
        const root = links[rootLinks[0]];

        const traverse = (link) => {
            for (const jointName in joints) {
                const joint = joints[jointName];
                if (joint.parent === link.name) {
                    const childLink = links[joint.child];
                    if (childLink) {
                        childLink.joint = joint;
                        childLink.matrix.copy(joint.matrix);
                        childLink.matrix.decompose(childLink.position, childLink.quaternion, childLink.scale);
                        link.add(childLink);
                        traverse(childLink);
                    }
                }
            }
        };
        traverse(root);

		root.joints = joints;
		root.links = links;
		root.updateMatrixWorld( true );
		return root;
	}
	parseLink( link ) {
        const name = link.getAttribute('name');
        const obj = new THREE.Object3D();
        obj.name = name;

        const visualEl = link.querySelector('visual');
        if (visualEl) {
            const visual = new THREE.Object3D();
            const originEl = visualEl.querySelector('origin');
            if (originEl) {
                const { xyz, rpy } = this.parseOrigin(originEl);
                visual.position.copy(xyz);
                visual.rotation.setFromVector3(rpy, 'XYZ');
            }

            const geometryEl = visualEl.querySelector('geometry > *');
            if (geometryEl) {
                const type = geometryEl.nodeName.toLowerCase();
                if (type === 'mesh') {
                    const filename = geometryEl.getAttribute('filename');
                    const scaleAttr = geometryEl.getAttribute('scale');
                    const scale = scaleAttr ? new Vector3(...scaleAttr.split(' ').map(Number)) : new Vector3(1, 1, 1);
                    const material = new MeshPhongMaterial({ color: 0xcccccc, shininess: 30 });
                    this.loadMeshCb(filename, scale, material, mesh => {
                        if (mesh) visual.add(mesh);
                    });
                }
            }
            obj.add(visual);
        }
        return obj;
	}
	parseJoint( joint ) {
		const name = joint.getAttribute( 'name' );
		const type = joint.getAttribute( 'type' );
		const parent = joint.querySelector( 'parent' ).getAttribute( 'link' );
		const child = joint.querySelector( 'child' ).getAttribute( 'link' );
		const originEl = joint.querySelector( 'origin' );
        let xyz = new Vector3();
        let rpy = new Vector3();
        if (originEl) {
            const res = this.parseOrigin(originEl);
            xyz = res.xyz; rpy = res.rpy;
        }
        const matrix = new Matrix4();
        matrix.makeRotationFromEuler(new THREE.Euler(rpy.x, rpy.y, rpy.z, 'XYZ'));
        matrix.setPosition(xyz);

        const axisEl = joint.querySelector('axis');
        const axis = axisEl ? new Vector3(...axisEl.getAttribute('xyz').split(' ').map(Number)) : new Vector3(1, 0, 0);

		return { name, type, parent, child, matrix, axis };
	}
	parseOrigin( origin ) {
		const xyzAttr = origin.getAttribute( 'xyz' );
		const rpyAttr = origin.getAttribute( 'rpy' );
		const xyz = xyzAttr ? new Vector3( ...xyzAttr.split( ' ' ).map( Number ) ) : new Vector3();
		const rpy = rpyAttr ? new Vector3( ...rpyAttr.split( ' ' ).map( Number ) ) : new Vector3();
		return { xyz, rpy };
	}
	defaultLoadMesh( path, scale, material, onComplete ) {
		const manager = this.manager;
        // 使用一个默认的路径映射来解析 "package://" URI
		this.packages = this.packages || {};
        this.packages.ur_description = this.packages.ur_description || '/urdf';

		const [ , pkg, rest ] = /package:\/\/(.*?)\/(.*)/.exec( path ) || [];
		if ( pkg ) {
			const pkgPath = this.packages[ pkg ];
			if ( pkgPath !== undefined ) { path = pkgPath + "/" + rest; }
            else { console.warn( `URDFLoader: Package '${ pkg }' not found.` ); onComplete( null ); return; }
		}

		if ( /\.stl$/i.test( path ) ) {
			const loader = new STLLoader( manager );
			loader.load( path, geom => {
                geom.computeVertexNormals();
				const mesh = new Mesh( geom, material );
				mesh.scale.copy( scale );
				onComplete( mesh );
			}, undefined, err => { console.error( `URDFLoader: Failed to load .stl file at ${path}`, err ); onComplete( null ); } );
		} else {
			console.warn( `URDFLoader: Mesh with unsupported type '${ path }' was not loaded.` );
			onComplete( null );
		}
	}
}
// =================================================================================================
// END: 内置的 URDFLoader 代码
// =================================================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM已加载，开始执行应用逻辑。");

    const ros = new ROSLIB.Ros({ url: 'ws://localhost:9090' });
    const statusElement = document.getElementById('connection-status');
    ros.on('connection', () => { statusElement.innerHTML = '已连接'; statusElement.style.color = 'green'; console.log('成功连接到websocket服务器。'); });
    ros.on('error', (error) => { statusElement.innerHTML = '连接错误'; statusElement.style.color = 'red'; console.error('连接websocket服务器出错: ', error); });
    ros.on('close', () => { statusElement.innerHTML = '已断开'; statusElement.style.color = 'red'; console.log('与websocket服务器的连接已关闭。'); });

    const viewerDiv = document.getElementById('viewer');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xcccccc);
    scene.add(new THREE.GridHelper(2, 10));
    scene.add(new THREE.AxesHelper(1));

    const camera = new THREE.PerspectiveCamera(60, viewerDiv.clientWidth / viewerDiv.clientHeight, 0.01, 1000);
    camera.position.set(1.5, 1.5, 1.5);
    
    const renderer = new THREE.WebGLRenderer({ antialias: true, logarithmicDepthBuffer: true });
    renderer.setSize(viewerDiv.clientWidth, viewerDiv.clientHeight);
    viewerDiv.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 0, 0.4);
    controls.update();

    const light = new THREE.DirectionalLight(0xffffff, 3.0);
    light.position.set(2, 2, 1);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0xffffff, 1.5));
    
    const loader = new URDFLoader();
    let robotModel = null;
    
    loader.load(
        '/urdf/ur5e.urdf',
        (robot) => {
            console.log("URDF模型加载成功:", robot);
            robotModel = robot;
            scene.add(robotModel);
        },
        undefined,
        (error) => { console.error("加载URDF时出错:", error); alert(error.message); }
    );

    function animate() { requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = viewerDiv.clientWidth / viewerDiv.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(viewerDiv.clientWidth, viewerDiv.clientHeight);
    });

    const jointStateListener = new ROSLIB.Topic({ ros: ros, name: '/joint_states', messageType: 'sensor_msgs/msg/JointState' });
    jointStateListener.subscribe((message) => {
        if (!robotModel) return;
        for (let i = 0; i < message.name.length; i++) {
            const jointName = message.name[i];
            const joint = robotModel.joints[jointName];
            if (joint) {
                const jointPosition = message.position[i];
                const link = robotModel.links[joint.child];
                if (link && joint.axis) {
                    const t = new THREE.Matrix4().makeTranslation(link.joint.matrix.getPosition().x, link.joint.matrix.getPosition().y, link.joint.matrix.getPosition().z);
                    const r = new THREE.Matrix4().makeRotationFromQuaternion(new THREE.Quaternion().setFromAxisAngle(joint.axis, jointPosition));
                    const o = new THREE.Matrix4().makeRotationFromQuaternion(new THREE.Quaternion().setFromRotationMatrix(link.joint.matrix));
                    link.matrix.copy(o).multiply(r).premultiply(t);
                    link.matrix.decompose(link.position, link.quaternion, link.scale);
                }
            }
        }
    });

    const actionClient = new ROSLIB.ActionClient({ ros: ros, serverName: '/scaled_joint_trajectory_controller/follow_joint_trajectory', actionName: 'control_msgs/action/FollowJointTrajectory' });
    document.getElementById('send-goal-btn').addEventListener('click', () => {
        const jointNames = [ 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint' ];
        const jointPositions = [
            parseFloat(document.getElementById('q1').value), parseFloat(document.getElementById('q2').value),
            parseFloat(document.getElementById('q3').value), parseFloat(document.getElementById('q4').value),
            parseFloat(document.getElementById('q5').value), parseFloat(document.getElementById('q6').value)
        ];
        const goal = new ROSLIB.Goal({ actionClient: actionClient, goalMessage: { trajectory: { joint_names: jointNames, points: [{ positions: jointPositions, time_from_start: { secs: 4, nsecs: 0 } }] } } });
        goal.send();
        console.log("已发送目标。");
    });
});
```

### 4.3 启动Web服务器与最终联调

1.  **打开一个新终端 (终端3)**。
2.  **进入前端项目目录**:
    ```bash
    cd ~/ur_web_control
    ```
3.  **启动一个简单的Python Web服务器**:
    ```bash
    python3 -m http.server 8000
    ```
4.  **最终访问**:
    打开你的Chrome或Firefox浏览器，访问 **http://localhost:8000**

    按下`F12`打开开发者工具，切换到“Console”(控制台)标签页。如果一切顺利，你将看到：
    -   “URDF模型加载成功” 的日志。
    -   网页上出现一个可以拖动、缩放的UR5e机械臂3D模型。
    -   网页左上角的连接状态显示为“已连接”。
    -   拖动滑块，然后点击“发送目标”按钮，Gazebo中的机械臂和网页上的模型会一起平滑地运动到指定位置！

---

## 总结

恭喜你！你已经成功地搭建并部署了一个完整的全栈机器人仿真项目。在这个过程中，你不仅掌握了Linux、ROS 2和Gazebo这些机器人领域的标准工具，还深入实践了现代Web前端开发，尤其是`three.js` 3D可视化技术。更重要的是，你亲身体验了解决复杂工程问题的全过程。希望这篇教程能成为你机器人开发之旅的坚实起点。
