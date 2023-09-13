SOURCE_IMAGE = 'imageRegistry/micropet-tap-fishes-sources'
LOCAL_PATH = os.getenv("LOCAL_PATH", default='.')
NAMESPACE = 'micropets-dev'

allow_k8s_contexts('aks-eu-tap-6')

k8s_custom_deploy(
    'fishes-python',
    apply_cmd="tanzu apps workload apply -f config/workload.yaml --update-strategy replace --debug --live-update" +
              " --local-path " + LOCAL_PATH +
              " --namespace " + NAMESPACE +
              " --yes --output yaml",

    delete_cmd="tanzu apps workload delete -f config/workload.yaml --namespace " + NAMESPACE + " --yes",
    deps=[''],
    container_selector='workload',
    live_update=[
      sync('.', '/workspace/'),
      run(
            'pip install -r /workspace/requirements.txt',
            trigger=['./workspace/requirements.txt']
        )
    ]
)

k8s_resource('fishes-python', port_forwards=["8080:8080"], extra_pod_selectors=[{'serving.knative.dev/service': 'fishes-python'}]) 