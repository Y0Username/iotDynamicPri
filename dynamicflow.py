import os

internet = '10.0.5.2'
edgeserver = '10.0.5.1'

level2Switches = ['s4','s5','s6','s7']
level3Switches = ['s2','s3']

s2_internet_hosts=['10.0.5.3','10.0.5.6']
s3_internet_hosts=['10.0.5.9','10.0.5.12']
s2_video_cameras=['10.0.5.4','10.0.5.7']
s3_video_cameras=['10.0.5.10','10.0.5.13']

def post_dynamic_flows():
    cmd = 'sudo ovs-ofctl mod-flows s2 ip,nw_dst='+edgeserver+',actions=set_queue:234,NORMAL'
    os.system(cmd)
    cmd = 'sudo ovs-ofctl mod-flows s3 ip,nw_dst='+edgeserver+',actions=set_queue:234,NORMAL'
    os.system(cmd)

    cmd = 'sudo ovs-ofctl mod-flows s2 ip,nw_dst='+internet+',actions=set_queue:123,NORMAL'
    os.system(cmd)
    cmd = 'sudo ovs-ofctl mod-flows s3 ip,nw_dst='+internet+',actions=set_queue:123,NORMAL'
    os.system(cmd)

if __name__ == '__main__':
    # This runs if this file is executed directly
    post_dynamic_flows()
