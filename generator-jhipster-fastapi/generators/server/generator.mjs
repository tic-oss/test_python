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
          { src: 'Dockerfile', dest: 'Dockerfile' },
          { src: 'requirements.txt', dest: 'requirements.txt' },
          { src: 'services/log_config.yaml', dest: 'services/log_config.yaml' },
          { src: 'main.py', dest: 'main.py' },
          { src: '.env', dest: '.env' },
          { src: 'README.md', dest: 'README.md' },

        
        ];
        const conditionalTemplates = [
          { condition: this.auth, src: 'services/keycloak.py', dest: 'services/keycloak.py' },
          { condition: this.rabbitmq, src: 'services/rabbitmq', dest: 'services/rabbitmq' },
          { condition: this.postgress, src: 'backend/database.py', dest: 'backend/database.py' },
          { condition: this.postgress, src: 'models/models.py', dest: 'models/models.py' },
          { condition: this.postgress, src: 'routers/postgres/posts.py', dest: 'routers/posts.py' },
          { condition: this.postgress, src: 'schemas/schema.py', dest: 'schemas/schema.py' },
          { condition: this.eureka, src: 'services/eureka.py', dest: 'services/eureka.py' },
          { condition: this.mongodb, src: 'backend/database.py', dest: 'backend/database.py' },
          { condition: this.mongodb, src: 'models/models.py', dest: 'models/models.py' },
          { condition: this.mongodb, src: 'routers/mongo/slack.py', dest: 'routers/slack.py' },
          { condition: this.eureka, src: 'services/eureka.py', dest: 'services/eureka.py' },

          
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
              this.templatePath('services/rabbitmq/consumer.py'),
              this.destinationPath('services/rabbitmq/' + 'RabbitMQConsumer' + server + 'To' + client + '.py'),
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
              this.templatePath('services/rabbitmq/producer.py'),
              this.destinationPath('services/rabbitmq/' + 'RabbitMQProducer' + server + 'To' + client + '.py'),
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