#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
BASE_DIR=`pwd -P`
popd > /dev/null

#############
# Functions
#############
function logging {
    echo "[INFO] $*"
}
function build_venv {
    if [ ! -d env ]; then
        virtualenv env
    fi
    . env/bin/activate
    pip install -r requirements.txt

}
function creator_db {
	logging "makemigrations"
	python "${BASE_DIR}/manage.py" "makemigrations"

	logging "migrate"
	python "${BASE_DIR}/manage.py" "migrate"

}
function write_data_db {
	logging "initdb.py"
	python "${BASE_DIR}/initdb.py"
}


function launch_webapp {
    python "${BASE_DIR}/manage.py" "runserver"
}
#############
# Main
#############
cd ${BASE_DIR}
OPT_ENV_FORCE=$1

build_venv

#创建数据库表，适合添加数据库后操作，能重复操作，不会破坏数据。
if [ "${OPT_ENV_FORCE}x" == "-cx" ];then    
    creator_db
fi
# 创建数据表、创建超级用户。
if [ "${OPT_ENV_FORCE}x" == "-cax" ];then    
    creator_db
    python "${BASE_DIR}/manage.py" "createsuperuser" #创建超级用户
fi

# 创建数据表,加载数据，其中有创建类等操作。因此，适合初次使用，不能重复操作。
if [ "${OPT_ENV_FORCE}x" == "-ix" ];then    
    creator_db
    write_data_db
fi

#删除数据库表，谨慎操作，删除数据不可恢复！！！
if [ "${OPT_ENV_FORCE}x" == "-dx" ];then
	rm -rf "${BASE_DIR}/db.sqlite3"
    logging "${BASE_DIR}/db.sqlite3"
fi

launch_webapp
