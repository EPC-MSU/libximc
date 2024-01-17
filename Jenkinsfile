def ciBuildingTag = false
script {
  if (env.TAG_NAME) {
    ciBuildingTag = true
  }
}

pipeline {
  agent { label "master" }

  parameters {
    booleanParam(name: 'DEBUG', defaultValue: false, description: 'Build with debug symbols')
    booleanParam(name: 'WITH_ARM', defaultValue: "${ciBuildingTag}", description: 'Enable build for ARM')
  }

  triggers {
    // enable weekly rebuilds
    cron('H H(6-9) * * 1')
  }

  options {
    disableConcurrentBuilds()
    parallelsAlwaysFailFast()
    timeout(time: 2, unit: 'HOURS')
  }

  environment {
    DEBUG = "${params.DEBUG}"
    SKIP_CLEAN_CHECKOUT = "yes"
  }

  stages {

    stage('init') {
      // execute at master
      steps {
        echo "Libximc init"
        echo "Param WITH_ARM=${params.WITH_ARM}"
        echo "Param DEBUG=${params.DEBUG}"
      }
    } // stage

    stage('build') {
      matrix {
        // limit execution at agent with matching label
        agent {
          label "${env.BUILDOS}"
        }
        axes {
          axis {
            name 'BUILDOS'
            values 'debian64', 'debian32', 'debianarm', 'suse64', 'suse32', 'win', 'osx'
          }
        }
        stages {

          stage('prebuild') {
            steps {
              echo "Pre"
              echo "Building at BUILDOS=${BUILDOS}"
            }
          } // stage

          stage('build-unix') {
            // Build for Linux and OSX agents
            // Condition: !(buildos=debianarm) || with_arm
            when { allOf {
              expression { isUnix() };
              anyOf {
                expression { env.BUILDOS != 'debianarm' };
                expression { params.WITH_ARM }
              };
              // avoid building tags on cron
              not { allOf { triggeredBy 'TimerTrigger'; buildingTag() } }
            } }
            steps {
              sh "./build-ci build"
              stash name: "result-${BUILDOS}", includes: "results-dist-*.tar"
            }
          } // stage

          stage('build-win') {
            // Build for Windows agents
            when { allOf {
              expression { !isUnix() };
              not { allOf { triggeredBy 'TimerTrigger'; buildingTag() } }
            } }
            steps {
              bat "build-ci.bat"
              stash name: "result-${BUILDOS}", includes: "results-dist-*.tar"
            }
          } // stage
        } // stages
        post {
          cleanup {
            // drop workspace for each matrix cell job
            cleanWs(notFailBuild: true)
          }
        }
      } // matrix
    } // stage
    
    stage('docs') {
      // execute at debian machine (BSD does not work)
      agent {
        label "debian64"
      }
      when {
        not { allOf { triggeredBy 'TimerTrigger'; buildingTag() } }
      }
      steps {
        // Just to be sure delete any local leftover files
        sh "rm -rf deps"
        sh "./build-ci docs"
        stash name: "result-docs", includes: "results-dist-*.tar"
      }
    } // stage


    stage('pack') {
      // execute on master
      when {
        not { allOf { triggeredBy 'TimerTrigger'; buildingTag() } }
      }
      steps {
        // Get all stashed archives
        unstash "result-debian64"
        unstash "result-debian32"
        unstash "result-suse64"
        unstash "result-suse32"
        unstash "result-win"
        unstash "result-osx"
        unstash "result-docs"
        script {
          if (params.WITH_ARM) {
            unstash "result-debianarm"
          }
        }
        sh "ls"
        sh "./build-ci unpack-stashes"
        sh "./build-ci py-binding"
        sh "./build-ci dist"
        archiveArtifacts artifacts: "dist/ximc*.tar.gz, dist/libximc_bindings_python-*.7z"
      }
    } // stage

  } // stages

  post {
    failure {
      echo "Failure, sending emails..."
      emailext body: '$DEFAULT_CONTENT',
               to: '$DEFAULT_RECIPIENTS',
               recipientProviders: [[$class: 'DevelopersRecipientProvider'],[$class: 'CulpritsRecipientProvider']],
               subject: '$DEFAULT_SUBJECT'
    }
    aborted {
      echo "Aborted, sending emails..."
      emailext body: '$DEFAULT_CONTENT',
               to: '$DEFAULT_RECIPIENTS',
               recipientProviders: [[$class: 'DevelopersRecipientProvider'],[$class: 'CulpritsRecipientProvider']],
               subject: '$DEFAULT_SUBJECT'
    }
    cleanup {
      // drop workspace for main job
      cleanWs(notFailBuild: true)
    }
  }
}

