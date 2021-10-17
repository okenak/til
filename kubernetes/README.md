
# minikube

## 起動
`minikube start`

## ノード接続
`minikube ssh`

## ダッシュボード起動
`minikube dashboard`

## ホスト側のローカルボリュームをマウント
`minikube mount /mnt/c/Users/kirak/Documents/workspace:/workspace`

## NodePortをホスト側に公開する
`minikube service nginx`

# Kubernetes

## Deployment

### maxUnavailable と maxSurge の詳細説明
- https://tech-lab.sios.jp/archives/18553
- https://kakakakakku.hatenablog.com/entry/2021/09/06/173014

# 参考資料
- [kubernetes.io](https://kubernetes.io/ja/)
- [The Kubectl Book](https://kubectl-book-ja.netlify.app/)
- [Kubernetes道場](https://cstoku.dev/tags/kubernetes/)
- [API Reference for Kubernetes v1.22](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/)