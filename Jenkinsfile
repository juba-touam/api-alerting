node {
    def GIT_COMMIT_HASH = ""

    stage("Checkout") {
        checkout scm
        GIT_COMMIT_HASH = sh(script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
    }

    stage('Install dependencies') {
        sh "ls -l ${env.WORKSPACE}"
        sh "docker run --rm -v ${env.WORKSPACE}:/app -w /app python:3.12 pip install -r /app/requirements.txt"
    }

    stage('Build Docker Image') {
        sh "docker build -t mchekini/api-alerting:$GIT_COMMIT_HASH ."
    }

    /*
    stage('Run Tests') {
        sh "docker run --rm -v ${env.WORKSPACE}:/app -w /app -e PYTHONPATH=/app mchekini/api-alerting:$GIT_COMMIT_HASH pytest || true"
    }
    */

    stage("Push Docker image") {
        withCredentials([usernamePassword(credentialsId: 'mchekini', passwordVariable: 'password', usernameVariable: 'username')]) {
            sh "docker login -u $username -p $password"
            sh "docker push mchekini/api-alerting:$GIT_COMMIT_HASH"
            sh "docker rmi mchekini/api-alerting:$GIT_COMMIT_HASH"
        }
    }
}
