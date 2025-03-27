

const Docker = require ('dockerode');
const docker = new Docker ({ host: 'http://localhost', port: 2375 });

async function createPythonContainer () {

    try {

        const container = await docker.createContainer ({

            Image: 'my_app_python:latest',  
            name: 'python_app',  

            Env: [

                'POSTGRES_HOST=localhost',
                'POSTGRES_DB=monitoreo',
                'POSTGRES_USER=postgres',
                'POSTGRES_PASSWORD=Opostgre2024'

            ],

            HostConfig: {

                Binds: ['C:/Users/PC/Desktop/PDWFSDC2024:/app'],
                NetworkMode: 'bridge',
                PortBindings: { '5001/tcp': [{ HostPort: '5001' }] }  
            },

            WorkingDir: '/app',
            Cmd: ['python', 'simulacion.py']

        });

        await container.start ();
        console.log ('CONTENEDOR DE Python INICIADO.');
        return container;

    } catch (err) {

        console.error ('ERROR AL CREAR EL CONTENEDOR DE Python:', err);

    }

}

createPythonContainer ();

