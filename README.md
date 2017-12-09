# iotDynamicPri
Dynamic Traffic Prioritization in IoT networks using SDN (ONOS Controller and Mininet Topology)

Run: `sudo mn --controller=remote,ip=192.168.56.101 --custom=iot_sdn.py --topo=mytopo`

### Description:
With the growth of IoT, the number of push-and-forget devices are increasing in traditional networks. These IoT devices are used for some application at the edge server or the cloud.
The goal of the project is to effectively prioritize traffic in a network which is mixture of IoT and traditional network. We leverage the application level knowledge of the IoT network to analyse the importance of the data. Using SDN, this application layer knowledge can be translated into traffic priorities.

For example, consider a campus network with motion sensor, camera and computers generating user traffic as shown in the topology. For a particular floor in the building, if the motion sensor detect any movement, the cameras should be given higher priority to stream HD video and web trffic should given lower priority. Similarly when there is no motion, the cameras should only stream SD video and we should not let the camera's UDP traffic take over the link bandwidth.

### Topology:

![Topology](https://github.com/Y0Username/iotDynamicPri/blob/master/topology.png)
