#!/bin/bash

# Определим тип файловой системы
FILESYSTEM=$(df -T | grep -E '(/$)' | awk '{print $2}')

# Создадим файл конфигурации Docker
DOCKER_CONFIG="/etc/docker/daemon.json"

# Проверим, существует ли уже файл конфигурации, и если нет, создадим его
if [ ! -f $DOCKER_CONFIG ]; then
  sudo touch $DOCKER_CONFIG
fi

# Выбираем подходящий драйвер хранения в зависимости от файловой системы
if [[ "$FILESYSTEM" == "overlay" ]]; then
    echo "Используем драйвер overlay2 для файловой системы overlay"
    sudo bash -c "echo '{ \"storage-driver\": \"overlay2\" }' > $DOCKER_CONFIG"
elif [[ "$FILESYSTEM" == "xfs" ]]; then
    echo "Используем драйвер overlay2 для файловой системы xfs"
    sudo bash -c "echo '{ \"storage-driver\": \"overlay2\" }' > $DOCKER_CONFIG"
elif [[ "$FILESYSTEM" == "ext4" ]]; then
    echo "Используем драйвер overlay2 для файловой системы ext4"
    sudo bash -c "echo '{ \"storage-driver\": \"overlay2\" }' > $DOCKER_CONFIG"
elif [[ "$FILESYSTEM" == "btrfs" ]]; then
    echo "Используем драйвер btrfs для файловой системы btrfs"
    sudo bash -c "echo '{ \"storage-driver\": \"btrfs\" }' > $DOCKER_CONFIG"
else
    echo "Неизвестная файловая система $FILESYSTEM. Пожалуйста, выберите подходящий драйвер вручную."
    exit 1
fi

# Перезапускаем Docker
echo "Перезапускаем Docker..."
sudo systemctl restart docker

# Проверяем состояние Docker
echo "Проверка состояния Docker..."
docker info
