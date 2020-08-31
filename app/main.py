from app import app
from flask import jsonify, render_template
import boto3


@app.route('/clusters.json')
def clusters():
    data = []
    emr = boto3.client('emr')

    clusters_iterator = emr.get_paginator('list_clusters').paginate(
        ClusterStates=['RUNNING', 'WAITING']
    )
    for clusters_page in clusters_iterator:
        for cluster in clusters_page['Clusters']:
            masters = emr.list_instances(
                ClusterId=cluster['Id'],
                InstanceGroupTypes=['MASTER'],
                InstanceStates=['RUNNING']
            )
            data.append({
                'id': cluster['Id'],
                'name': cluster['Name'],
                'status': cluster['Status']['State'],
                'master_private_ip': masters['Instances'][0]['PrivateIpAddress']
            })

    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')
