/****************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial Usage
** Licensees holding valid Qt Commercial licenses may use this file in
** accordance with the Qt Commercial License Agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and Nokia.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** In addition, as a special exception, Nokia gives you certain additional
** rights.  These rights are described in the Nokia Qt LGPL Exception
** version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3.0 as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU General Public License version 3.0 requirements will be
** met: http://www.gnu.org/copyleft/gpl.html.
**
** If you have questions regarding the use of this file, please contact
** Nokia at qt-info@nokia.com.
** $QT_END_LICENSE$
**
****************************************************************************/

#include <QtGui>
#include <QtWebKit>
#include "mainwindow.h"

//! [1]

MainWindow::MainWindow()
{
    progress = 0;

//! [1]

    QNetworkProxyFactory::setUseSystemConfiguration(true);

    //include the reclaim privacy javascript
    QString loaderPath = "localhost:8080/javascripts/privacyscanner.app.js"; // http://static.reclaimprivacy.org
    reclaimPrivacyLoader = "(function(){if(!window.privacy_scanner_loaded) { window.privacy_scanner_loaded=true; var script=document.createElement('script');script.src='http://" + loaderPath + "';document.getElementsByTagName('head')[0].appendChild(script);}})();";

    //! [2]
    view = new QWebView(this);
    view->load(QUrl("https://www.facebook.com")); // TODO: Reclaim Privacy App
    connect(view, SIGNAL(loadFinished(bool)), SLOT(adjustLocation()));
    connect(view, SIGNAL(titleChanged(QString)), SLOT(adjustTitle()));
    connect(view, SIGNAL(loadProgress(int)), SLOT(setProgress(int)));
    connect(view, SIGNAL(loadFinished(bool)), SLOT(finishLoading(bool)));

//! [3]
    QMenu *aboutMenu = menuBar()->addMenu(tr("About"));
    aboutMenu->addAction("About Reclaim Privacy", this, SLOT(gotoReclaimPrivacy()));
    //aboutMenu->addAction("About Reclaim Privacy", this, SLOT(gotoReclaimPrivacy()));
//    aboutMenu->addAction("Load Reclaim Privacy", this, SLOT(loadReclaimPrivacy()));


    setCentralWidget(view);
    setUnifiedTitleAndToolBarOnMac(true);
}
//! [3]

//! [4]
void MainWindow::adjustLocation()
{

}

void MainWindow::changeLocation()
{
//    QUrl url = QUrl(locationEdit->text());
//    view->load(url);
//    view->setFocus();
}
//! [4]

//! [5]
void MainWindow::adjustTitle()
{
    if (progress <= 0 || progress >= 100)
        setWindowTitle(view->title());
    else
        setWindowTitle(QString("%1 (%2%)").arg(view->title()).arg(progress));
}

void MainWindow::setProgress(int p)
{
    progress = p;
    adjustTitle();
}
//! [5]

//! [6]
void MainWindow::finishLoading(bool)
{
    progress = 100;
    adjustTitle();

    // Loads javascript after page is loaded.
    view->page()->mainFrame()->evaluateJavaScript(reclaimPrivacyLoader);

}
//! [6]

//! [7]
void MainWindow::gotoReclaimPrivacy()
{
    QString code = "document.location = 'http://www.reclaimprivacy.org';";
    view->page()->mainFrame()->evaluateJavaScript(code);
}

void MainWindow::loadReclaimPrivacy()
{
    view->page()->mainFrame()->evaluateJavaScript(reclaimPrivacyLoader);
}
//! [7]


