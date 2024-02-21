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
          // restServer: restServer,
          // restClient: restClient,
          // rabbitmqServer: rabbitmqServer,
          // rabbitmqClient: rabbitmqClient,
        };

        const templatePaths = [
          { src: 'posts', dest: 'posts' },
          { src: 'venv', dest: 'venv' },
          { src: 'Dockerfile', dest: 'Dockerfile' },
          { src: 'log_config.yaml', dest: 'log_config.yaml' },
          { src: 'main.py', dest: 'main.py' },
          { src: 'requirements.txt', dest: 'requirements.txt' },
          { src: 'README.md', dest: 'README.md' },
        
        ];
        const conditionalTemplates = [
          { condition: this.auth, src: 'auth', dest: 'auth' },
          { condition: this.rabbitmq, src: 'rabbitmq', dest: 'rabbitmq' },
          { condition: this.postgress, src: 'db/postgres/database.py', dest: 'db/postgres/database.py' },
          { condition: this.postgress, src: 'db/postgres/models.py', dest: 'db/postgres/models.py' },
          { condition: this.postgress, src: 'db/postgres/schema.py', dest: 'db/postgres/schema.py' },
          { condition: this.mongodb, src: 'db/mongo/database.py', dest: 'db/mongo/database.py' },
          { condition: this.mongodb, src: 'db/mongo/models.py', dest: 'db/mongo/models.py' },
          { condition: this.eureka, src: 'eureka.py', dest: 'eureka.py' },+
          
        ];
        templatePaths.forEach(({ src, dest }) => {
          this.fs.copyTpl(this.templatePath(src), this.destinationPath(dest), templateVariables);
        });
        conditionalTemplates.forEach(({ condition, src, dest }) => {
          if (condition) {
            this.fs.copyTpl(this.templatePath(src), this.destinationPath(dest), templateVariables);
          }
        });
        // if (rabbitmqServer?.length) {
        //   for (var i = 0; i < rabbitmqServer.length; i++) {
        //     var server = rabbitmqServer[i].charAt(0).toUpperCase() + rabbitmqServer[i].slice(1);
        //     var client = this.baseName.charAt(0).toUpperCase() + this.baseName.slice(1);
        //     this.fs.copyTpl(
        //       this.templatePath('rabbitmq/consumer.py'),
        //       this.destinationPath('rabbitmq/' + 'RabbitMQConsumer' + server + 'To' + client + '.py'),
        //       {
        //         packageName: this.packageName,
        //         rabbitmqServer: server,
        //         rabbitmqClient: client,
        //         baseName: this.baseName,
        //       }
        //     );
        //   }
        // }
        // if (rabbitmqClient?.length) {
        //   for (var i = 0; i < rabbitmqClient.length; i++) {
        //     var server = this.baseName.charAt(0).toUpperCase() + this.baseName.slice(1);
        //     var client = rabbitmqClient[i].charAt(0).toUpperCase() + rabbitmqClient[i].slice(1);
        //     this.fs.copyTpl(
        //       this.templatePath('rabbitmq/producer.py'),
        //       this.destinationPath('rabbitmq/' + 'RabbitMQProducer' + server + 'To' + client + '.py'),
        //       {
        //         packageName: this.packageName,
        //         rabbitmqClient: client,
        //         rabbitmqServer: server,
        //         baseName: this.baseName,
        //       }
        //     );
        //   }
        // }
      },
    };
  }
}