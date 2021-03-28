//def name      = "main"
def git_branch      = "staging"
def namespace       = "staging"
def gitUrl          = "https://github.com/pro-ghanem/flask-api"
def serviceName     = "flask-api"
def imageTag        = "${serviceName}:${namespace}_${BUILD_NUMBER}"
//def registryId      = 604159183131
def awsRegion       = "ap-southeast-1"
def ecrUrl          = "686777881901.dkr.ecr.ap-southeast-1.amazonaws.com"
//def ecr             = " 686777881901.dkr.ecr.ap-southeast-1.amazonaws.com"
//def awsProfile      = "default"
def k8sContext      = "arn:aws:eks:ap-southeast-1:686777881901:cluster/Prod-cluster"
def awsCredsId      = "ecr-credentials"
def helmDir         = "helm"
def gitCred         = "chadminfrontend"
node {
  try {
    notifyBuild('STARTED')
    stage ("Checkout"){
      checkout([$class: 'GitSCM', branches: [[name: "${git_branch}"]], extensions: [], userRemoteConfigs: [[credentialsId: "" , url: "${gitUrl}"]]])    
    
withCredentials([file(credentialsId: 'csvstagdocker', variable: 'csvstagdocker')]) {
    
  sh  " mv \$csvstagdocker Dockerfile"
   } 
    
    }

    stage("Get the Commit ID"){
      sh "git rev-parse --short HEAD > .git/commit-id"
      commitId= readFile('.git/commit-id').trim()
    }

	stage('compile')

	{ sh label: '', script: '''  npm install'''}

    stage ('Build Docker Image'){
      sh "docker build -t ${imageTag} ."
    }

    stage ('tag Image With Commit ID '){
      sh "docker tag ${imageTag} ${serviceName}:${namespace}-${commitId}"
    }

 //   stage ('login to ecr '){   >>> NO NEED FOR LOGIN TO ECR BECAUSE WE ALLREADY PUSSING USING ECR CERDENTIALS
//      sh "aws ecr get-login --registry-ids ${registryId} --region ${awsRegion} --no-include-email"
//sh "aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin ${ecr}"
//    }

//    stage ('Swtich context '){
//      sh "export AWS_DEFAULT_PROFILE=${awsProfile}"
//      sh "kubectl config use-context ${k8sContext}"
//    }

    stage('Push Docker Image With Commit ID To ECR'){
      docker.withRegistry("https://${ecrUrl}/${serviceName}", "ecr:${awsRegion}:${awsCredsId}") {
      docker.image("${serviceName}:${namespace}-${commitId}").push("${namespace}-${commitId}")
      }
    }

    stage ("Deploy ${serviceName} to ${namespace} Enviroment"){
      sh "helm -n staging upgrade ${serviceName} ${helmDir} --set image.repository=${ecrUrl}/${serviceName} --set image.tag=${namespace}-${commitId} --set namespace=${namespace}"
      //sh ("kubectl -ndev set image deployment/fn-grower-dev fn-grower-dev=${ecrUrl}/${serviceName}:${NAMESPACE}-${GIT_COMMIT_ID}")
      //sh("kubectl -n ${NAMESPACE} rollout status deploy/fn-grower-dev")
      }

 stage('Remove local images') {
    // remove docker images
    sh("docker rmi -f ${serviceName}:${namespace}-${commitId} || :")
    sh("docker rmi -f ${serviceName}:${namespace}-${commitId} || :")
    sh("docker rmi -f ${ecrUrl}/${serviceName}:${namespace}-${commitId} || :")
      }
 // stage ('cleanup'){
 // cleanWs()
// }
}
catch (e) {
    // If there was an exception thrown, the build failed
    currentBuild.result = "FAILED"
    throw e
  } finally {
    // Success or failure, always send notifications
    notifyBuild(currentBuild.result)
  }
  }
def notifyBuild(String buildStatus = 'STARTED') {
  // build status of null means successful
  buildStatus =  buildStatus ?: 'SUCCESSFUL'
  // Default values
  def colorName = 'RED'
  def colorCode = '#FF0000'
  def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
  def summary = "${subject} (${env.BUILD_URL})"
  // Override default values based on build status
  if (buildStatus == 'STARTED') {
    color = 'YELLOW'
    colorCode = '#FFFF00'
  } else if (buildStatus == 'SUCCESSFUL') {
    color = 'GREEN'
    colorCode = '#00FF00'
  } else {
    color = 'RED'
    colorCode = '#FF0000'
  }
  // deleteDir() 

  // Send notifications
  //slackSend (color: colorCode, message: summary)
 }
