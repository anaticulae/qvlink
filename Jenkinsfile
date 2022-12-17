@Library('caelum@a1411f1288b8bc739b27c2e76f50554a6fdcda8c') _

pipeline {
    agent {
        docker {
            image '169.254.149.20:6001/arch_python_git_baw:v1.36.0'
        }
    }
    environment{
        SHARED_READY='/tmp/dev/tmp/shared/ready/'
        SHARED_TODO='/tmp/dev/tmp/shared/todo/'
    }
    stages{
        stage('integrate'){
            steps{script{baw.integrate()}}
        }
        stage('setup'){
            steps{script{baw.setup()}}
        }
        stage('test'){
            failFast true
            parallel{
                stage('doc'){
                    steps{
                        script{baw.doctest()}
                    }
                }
                stage('fast'){
                    steps{
                        script{baw.fast()}
                    }
                }
                stage('long'){
                    steps{
                        script{baw.longrun()}
                    }
                }
            }
        }
        stage('all'){
            steps{
                script{baw.all()}
            }
        }
        stage('quality'){
            failFast true
            parallel{
                stage('lint'){
                    steps{
                        script{baw.lint()}
                    }
                }
                stage('format'){
                    steps{
                        script{baw.format()}
                    }
                }
            }
        }
        stage('pre-release'){
            when{not{branch 'master'}}
            steps{sh 'baw publish --pre'}
        }
        stage('release'){
            steps{
                script{publish.release()}
            }
        }
    }
}
