import os

internet = '10.0.5.2'
edgeserver = '10.0.5.1'

level2Switches = ['s4','s5','s6','s7']
level3Switches = ['s2','s3']

s2_internet_hosts=['10.0.5.3','10.0.5.6']
s3_internet_hosts=['10.0.5.9','10.0.5.12']
s2_video_cameras=['10.0.5.4','10.0.5.7']
s3_video_cameras=['10.0.5.10','10.0.5.13']

#Queue 123 is low priority
#Queue 234 is high priority

def post_static_flows():
    for host in s2_internet_hosts:
        #TODO
        cmd = 'sudo ovs-ofctl add-flow s2 ip,priority=6653,nw_src='+host+',nw_dst='+internet+',idle_timeout=0,actions=set_queue:234,normal'
        os.system(cmd)
    for host in s3_internet_hosts:
        #TODO
        cmd = 'sudo ovs-ofctl add-flow s3 ip,priority=6653,nw_src='+host+',nw_dst='+internet+',idle_timeout=0,actions=set_queue:234,normal'
        os.system(cmd)

    for camera in s2_video_cameras:
        #TODO
        cmd = 'sudo ovs-ofctl add-flow s2 ip,priority=6653,nw_src='+camera+',nw_dst='+edgeserver+',idle_timeout=0,actions=set_queue:123,normal'
        os.system(cmd)
    for camera in s3_video_cameras:
        #TODO
        cmd = 'sudo ovs-ofctl add-flow s3 ip,priority=6653,nw_src='+camera+',nw_dst='+edgeserver+',idle_timeout=0,actions=set_queue:123,normal'
        os.system(cmd)

if __name__ == '__main__':
    # This runs if this file is executed directly
    post_static_flows()
