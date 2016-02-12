#!/bin/bash

echo "#!/bin/bash" > setup_with_env.sh
echo "bash setup.sh $1 $2 $3" >> setup_with_env.sh
chmod a+x setup_with_env.sh
