import chalk from 'chalk';
import yosay from 'yosay';
import ServerGenerator from 'generator-jhipster/generators/server';
import { askForServerSideOpts } from './prompts.mjs';
import { loadCommunicationConfigs, findConfigByBaseName, deleteUnwantedFiles } from './util.mjs';

export default class extends ServerGenerator {
  constructor(args, opts, features) {
    super(args, opts, features);

    if (this.options.help) return;

    if (!this.options.jhipsterContext) {
      throw new Error(`This is a JHipster blueprint and should be used only like ${chalk.yellow('jhipster --blueprints fastapi')}`);
    }
  }

  get [ServerGenerator.INITIALIZING]() {
    return {
    };
  }

  get [ServerGenerator.PROMPTING]() {
    return {
      prompting() {
        this.log(yosay(`${chalk.red('fastapi-blueprint')}`));
      },
      askForServerSideOpts,
      loadCommunicationConfigs,
    };
  }

  get [ServerGenerator.CONFIGURING]() {
    return {
    };
  }

  get [ServerGenerator.COMPOSING]() {
    return {
    };
  }

  get [ServerGenerator.LOADING]() {
    return {
    };
  }

  get [ServerGenerator.PREPARING]() {
    return {
    };
  }

  get [ServerGenerator.CONFIGURING_EACH_ENTITY]() {
    return {
    };
  }

  get [ServerGenerator.LOADING_ENTITIES]() {
    return {
    };
  }

  get [ServerGenerator.PREPARING_EACH_ENTITY]() {
    return {
    };
  }

  get [ServerGenerator.PREPARING_EACH_ENTITY_FIELD]() {
    return {
    };
  }

  get [ServerGenerator.PREPARING_EACH_ENTITY_RELATIONSHIP]() {
    return {
    };
  }

  get [ServerGenerator.POST_PREPARING_EACH_ENTITY]() {
    return {
    };
  }

  get [ServerGenerator.DEFAULT]() {
    return {
    };
  }

  get [ServerGenerator.WRITING]() {
    return {
    };
  }

  get [ServerGenerator.WRITING_ENTITIES]() {
    return {
    };
  }

  get [ServerGenerator.POST_WRITING]() {
    return {
    };
  }

  get [ServerGenerator.POST_WRITING_ENTITIES]() {
    return {
    };
  }

  get [ServerGenerator.INSTALL]() {
    return {
    };
  }

  get [ServerGenerator.POST_INSTALL]() {
    return {
    };
  }

  get [ServerGenerator.END]() {
    return {
      endTemplateTask() {
        deleteUnwantedFiles.call(this);
      },
      writing() {
        const matchingScenarios = findConfigByBaseName(this.baseName);

        if (matchingScenarios.length > 0) {
          var restServer = [],
            restClient,
            rabbitmqServer = [],
            rabbitmqClient = [];

          for (var options of matchingScenarios) {
            if (options.framework === 'rest-api') {
              if (options.server) {
                restServer.push(options.server);
              }
              if (options.client) {
                restClient = options.client;
              }
            } else if (options.framework === 'rabbitmq') {
              if (options.server) {
                rabbitmqServer.push(options.server);
              }
              if (options.client) {
                rabbitmqClient.push(options.client);
              }
            }
          }
        }
        const templateVariables = {
          serverPort: this.serverPort,
          packageName: this.packageName,
          baseName: this.baseName,
          auth: this.auth,
          eureka: this.eureka,
          rabbitmq: this.rabbitmq,
          postgresql: this.postgress,
          mongodb: this.mongodb,
          restServer: restServer,
          restClient: restClient,
          rabbitmqServer: rabbitmqServer,
          rabbitmqClient: rabbitmqClient,
        };

        const templatePaths = [
          { src: 'docker', dest: 'docker' },
          { src: 'proto', dest: 'proto' },
          { src: 'go.mod', dest: 'go.mod' },
          { src: 'main.go', dest: 'main.go' },
          { src: 'Dockerfile', dest: 'Dockerfile' },
          { src: 'Makefile', dest: 'Makefile' },
          { src: 'README.md', dest: 'README.md' },
          { src: 'config', dest: 'config' },
          { src: 'resources', dest: 'resources' },
          { src: 'controllers', dest: 'controllers' },
        ];
        const conditionalTemplates = [
          { condition: this.auth, src: 'auth', dest: 'auth' },
          { condition: this.postgress, src: 'handler/db.go', dest: 'handler/db.go' },
          { condition: this.mongodb, src: 'handler/mongodb.go', dest: 'handler/mongodb.go' },
          { condition: this.postgress, src: 'db/config.go', dest: 'db/config.go' },
          { condition: this.mongodb, src: 'db/mongoconfig.go', dest: 'db/mongoconfig.go' },
          { condition: this.eureka, src: 'eurekaregistry/helper', dest: 'eurekaregistry/helper' },
          { condition: this.eureka, src: 'eurekaregistry/DiscoveryManager.go', dest: 'eurekaregistry/DiscoveryManager.go' },
          { condition: this.eureka, src: 'eurekaregistry/RegistrationManager.go', dest: 'eurekaregistry/RegistrationManager.go' },
          { condition: this.eureka, src: 'eurekaregistry/EurekaRegistrationManager.go', dest: 'eurekaregistry/EurekaRegistrationManager.go' },
          { condition: restServer?.length, src: 'eurekaregistry/ServiceDiscovery.go',dest: 'eurekaregistry/ServiceDiscovery.go' },
          { condition: this.postgress, src: 'migrate', dest: 'migrate' },+
          { condition: this.rabbitmq, src: 'rabbitmq', dest: 'rabbitmq' },
        ];
        templatePaths.forEach(({ src, dest }) => {
          this.fs.copyTpl(this.templatePath(src), this.destinationPath(dest), templateVariables);
        });
        conditionalTemplates.forEach(({ condition, src, dest }) => {
          if (condition) {
            this.fs.copyTpl(this.templatePath(src), this.destinationPath(dest), templateVariables);
          }
        });
        if (rabbitmqServer?.length) {
          for (var i = 0; i < rabbitmqServer.length; i++) {
            var server = rabbitmqServer[i].charAt(0).toUpperCase() + rabbitmqServer[i].slice(1);
            var client = this.baseName.charAt(0).toUpperCase() + this.baseName.slice(1);
            this.fs.copyTpl(
              this.templatePath('rabbitmq/consumer.py'),
              this.destinationPath('rabbitmq/' + 'RabbitMQConsumer' + server + 'To' + client + '.py'),
              {
                packageName: this.packageName,
                rabbitmqServer: server,
                rabbitmqClient: client,
                baseName: this.baseName,
              }
            );
          }
        }
        if (rabbitmqClient?.length) {
          for (var i = 0; i < rabbitmqClient.length; i++) {
            var server = this.baseName.charAt(0).toUpperCase() + this.baseName.slice(1);
            var client = rabbitmqClient[i].charAt(0).toUpperCase() + rabbitmqClient[i].slice(1);
            this.fs.copyTpl(
              this.templatePath('rabbitmq/producer.py'),
              this.destinationPath('rabbitmq/' + 'RabbitMQProducer' + server + 'To' + client + '.py'),
              {
                packageName: this.packageName,
                rabbitmqClient: client,
                rabbitmqServer: server,
                baseName: this.baseName,
              }
            );
          }
        }
      },
    };
  }
}