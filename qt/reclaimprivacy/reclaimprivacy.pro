QT      +=  webkit network
HEADERS =   mainwindow.h
SOURCES =   main.cpp \
            mainwindow.cpp
RESOURCES = jquery.qrc

# install
target.path = /Users/ben/git/reclaimprivacy
sources.files = $$SOURCES $$HEADERS $$RESOURCES *.pro
sources.path = /Users/ben/git/reclaimprivacy
INSTALLS += target sources

symbian {
    TARGET.UID3 = 0xA000CF6C
    include($$QT_SOURCE_TREE/examples/symbianpkgrules.pri)
}
