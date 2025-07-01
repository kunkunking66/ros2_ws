cmake_minimum_required(VERSION 3.8)
project(ed6_description)

# 查找ament_cmake，這是構建ROS 2包的基礎
find_package(ament_cmake REQUIRED)
# 查找xacro，因爲我們在launch文件中用到了它
find_package(xacro REQUIRED)

# 這是解決問題的關鍵部分：安裝文件夾
# 將 launch 文件夾安裝到 share/ed6_description/launch
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# 將 urdf 文件夾安裝到 share/ed6_description/urdf
install(
  DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

# 將 meshes 文件夾安裝到 share/ed6_description/meshes
install(
  DIRECTORY meshes
  DESTINATION share/${PROJECT_NAME}
)

# 將 config 文件夾安裝到 share/ed6_description/config
install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

# 同時，必須安裝package.xml文件
install(
  FILES package.xml
  DESTINATION share/${PROJECT_NAME}
)

# ament_package()宏是所有ament包必須的
ament_package()
