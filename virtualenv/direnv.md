<https://github.com/direnv/direnv>
# direnv
###  OS: centos7

#### 1. install 
    source from: https://dl.equinox.io/zimbatm/direnv/stable

#### 2.setup
    rpm install xxxx.rpm
#### 2.1 修改~/.bashrc(加入以下这行)
    eval "$(direnv hook bash)"
####  另外还支持zsh, fish, tcsh
    eval "$(direnv hook xxx)"
    note: 对应xxx就是各自shell的名字

## 2.2 新建目录，生成虚拟工作区
    mkdir test
    cd test
    vim .envrc
        layout python ## 写入.envrc
    direnv allow .
## 然后就可以切换目录一样切换env了
