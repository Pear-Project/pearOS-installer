/********************************************************************************
** Form generated from reading UI file 'ChoicePage.ui'
**
** Created by: Qt User Interface Compiler version 6.11.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CHOICEPAGE_H
#define UI_CHOICEPAGE_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QTreeView>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include "gui/EncryptWidget.h"

QT_BEGIN_NAMESPACE

class Ui_ChoicePage
{
public:
    QHBoxLayout *m_outerLayout;
    QWidget *sidebarPanel;
    QVBoxLayout *sidebarPanelLayout;
    QTreeView *deviceSidebarView;
    QWidget *mainContentWidget;
    QVBoxLayout *m_mainLayout;
    QHBoxLayout *topToolbarLayout;
    QToolButton *viewMenuButton;
    QSpacerItem *topToolbarSpacer;
    QHBoxLayout *m_drivesLayout;
    QLabel *m_drivesLabel;
    QVBoxLayout *m_rightLayout;
    QLabel *m_messageLabel;
    QScrollArea *m_itemsScrollArea;
    QWidget *scrollAreaWidgetContents;
    QVBoxLayout *m_itemsLayout;
    QFrame *hLine;
    EncryptWidget *m_encryptWidget;
    QCheckBox *m_reuseHomeCheckBox;
    QLabel *m_selectLabel;
    QHBoxLayout *diskHeaderLayout;
    QLabel *diskHeaderIcon;
    QVBoxLayout *diskHeaderTextLayout;
    QLabel *diskHeaderTitle;
    QLabel *diskHeaderSubtitle;
    QSpacerItem *diskHeaderSpacer;
    QLabel *diskHeaderCapacityBadge;
    QFrame *diskHeaderSeparator;
    QGridLayout *beforeAfterGridLayout;
    QVBoxLayout *verticalLayout_2;
    QSpacerItem *verticalSpacer_2;
    QLabel *m_previewAfterLabel;
    QVBoxLayout *verticalLayout;
    QSpacerItem *verticalSpacer;
    QLabel *m_previewBeforeLabel;
    QWidget *m_previewBeforeFrame;
    QWidget *m_previewAfterFrame;
    QWidget *diskInfoPanel;
    QGridLayout *diskInfoGrid;
    QFrame *diskInfoVSeparator;
    QLabel *label_location;
    QLabel *locationValueLabel;
    QLabel *label_capacity;
    QLabel *capacityValueLabel;
    QFrame *diskInfoHSeparator1Left;
    QFrame *diskInfoHSeparator1Right;
    QLabel *label_connection;
    QLabel *connectionValueLabel;
    QLabel *label_child_count;
    QLabel *childCountValueLabel;
    QFrame *diskInfoHSeparator2Left;
    QFrame *diskInfoHSeparator2Right;
    QLabel *label_partition_map;
    QLabel *partitionMapValueLabel;
    QLabel *label_type;
    QLabel *typeValueLabel;
    QFrame *diskInfoHSeparator3Left;
    QFrame *diskInfoHSeparator3Right;
    QLabel *label_smart;
    QLabel *smartValueLabel;
    QLabel *label_device;
    QLabel *deviceValueLabel;
    QSpacerItem *rightLayoutTrailingSpacer;

    void setupUi(QWidget *ChoicePage)
    {
        if (ChoicePage->objectName().isEmpty())
            ChoicePage->setObjectName("ChoicePage");
        ChoicePage->resize(743, 512);
        ChoicePage->setWindowTitle(QString::fromUtf8("Form"));
        m_outerLayout = new QHBoxLayout(ChoicePage);
        m_outerLayout->setSpacing(0);
        m_outerLayout->setContentsMargins(0, 0, 0, 0);
        m_outerLayout->setObjectName("m_outerLayout");
        sidebarPanel = new QWidget(ChoicePage);
        sidebarPanel->setObjectName("sidebarPanel");
        sidebarPanel->setMinimumSize(QSize(180, 0));
        sidebarPanel->setMaximumSize(QSize(260, 16777215));
        sidebarPanelLayout = new QVBoxLayout(sidebarPanel);
        sidebarPanelLayout->setSpacing(0);
        sidebarPanelLayout->setContentsMargins(0, 0, 0, 0);
        sidebarPanelLayout->setObjectName("sidebarPanelLayout");
        deviceSidebarView = new QTreeView(sidebarPanel);
        deviceSidebarView->setObjectName("deviceSidebarView");
        deviceSidebarView->setEditTriggers(QAbstractItemView::NoEditTriggers);
        deviceSidebarView->setFrameShape(QFrame::NoFrame);
        deviceSidebarView->setHeaderHidden(true);
        deviceSidebarView->setRootIsDecorated(true);
        deviceSidebarView->setIndentation(14);

        sidebarPanelLayout->addWidget(deviceSidebarView);


        m_outerLayout->addWidget(sidebarPanel);

        mainContentWidget = new QWidget(ChoicePage);
        mainContentWidget->setObjectName("mainContentWidget");
        m_mainLayout = new QVBoxLayout(mainContentWidget);
        m_mainLayout->setObjectName("m_mainLayout");
        m_mainLayout->setContentsMargins(-1, -1, -1, 0);
        topToolbarLayout = new QHBoxLayout();
        topToolbarLayout->setObjectName("topToolbarLayout");
        viewMenuButton = new QToolButton(mainContentWidget);
        viewMenuButton->setObjectName("viewMenuButton");
        viewMenuButton->setPopupMode(QToolButton::InstantPopup);
        viewMenuButton->setToolButtonStyle(Qt::ToolButtonTextOnly);

        topToolbarLayout->addWidget(viewMenuButton);

        topToolbarSpacer = new QSpacerItem(10, 10, QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Minimum);

        topToolbarLayout->addItem(topToolbarSpacer);


        m_mainLayout->addLayout(topToolbarLayout);

        m_drivesLayout = new QHBoxLayout();
        m_drivesLayout->setObjectName("m_drivesLayout");
        m_drivesLabel = new QLabel(mainContentWidget);
        m_drivesLabel->setObjectName("m_drivesLabel");
#if QT_CONFIG(tooltip)
        m_drivesLabel->setToolTip(QString::fromUtf8(""));
#endif // QT_CONFIG(tooltip)
        m_drivesLabel->setText(QString::fromUtf8("<m_drivesLabel>"));

        m_drivesLayout->addWidget(m_drivesLabel);


        m_mainLayout->addLayout(m_drivesLayout);

        m_rightLayout = new QVBoxLayout();
        m_rightLayout->setObjectName("m_rightLayout");
        m_messageLabel = new QLabel(mainContentWidget);
        m_messageLabel->setObjectName("m_messageLabel");
#if QT_CONFIG(tooltip)
        m_messageLabel->setToolTip(QString::fromUtf8(""));
#endif // QT_CONFIG(tooltip)
        m_messageLabel->setText(QString::fromUtf8("<m_messageLabel>"));

        m_rightLayout->addWidget(m_messageLabel);

        m_itemsScrollArea = new QScrollArea(mainContentWidget);
        m_itemsScrollArea->setObjectName("m_itemsScrollArea");
        m_itemsScrollArea->setFrameShape(QFrame::NoFrame);
        m_itemsScrollArea->setFrameShadow(QFrame::Plain);
        m_itemsScrollArea->setLineWidth(0);
        m_itemsScrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName("scrollAreaWidgetContents");
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 729, 233));
        m_itemsLayout = new QVBoxLayout(scrollAreaWidgetContents);
        m_itemsLayout->setObjectName("m_itemsLayout");
        m_itemsLayout->setContentsMargins(0, 0, 0, 0);
        m_itemsScrollArea->setWidget(scrollAreaWidgetContents);

        m_rightLayout->addWidget(m_itemsScrollArea);

        hLine = new QFrame(mainContentWidget);
        hLine->setObjectName("hLine");
        hLine->setFrameShape(QFrame::HLine);
        hLine->setFrameShadow(QFrame::Raised);

        m_rightLayout->addWidget(hLine);

        m_encryptWidget = new EncryptWidget(mainContentWidget);
        m_encryptWidget->setObjectName("m_encryptWidget");

        m_rightLayout->addWidget(m_encryptWidget);

        m_reuseHomeCheckBox = new QCheckBox(mainContentWidget);
        m_reuseHomeCheckBox->setObjectName("m_reuseHomeCheckBox");
        m_reuseHomeCheckBox->setText(QString::fromUtf8("<m_reuseHomeCheckBox>"));

        m_rightLayout->addWidget(m_reuseHomeCheckBox);

        m_selectLabel = new QLabel(mainContentWidget);
        m_selectLabel->setObjectName("m_selectLabel");
        m_selectLabel->setText(QString::fromUtf8(""));

        m_rightLayout->addWidget(m_selectLabel);

        diskHeaderLayout = new QHBoxLayout();
        diskHeaderLayout->setObjectName("diskHeaderLayout");
        diskHeaderIcon = new QLabel(mainContentWidget);
        diskHeaderIcon->setObjectName("diskHeaderIcon");
        diskHeaderIcon->setMinimumSize(QSize(64, 64));
        diskHeaderIcon->setMaximumSize(QSize(64, 64));

        diskHeaderLayout->addWidget(diskHeaderIcon);

        diskHeaderTextLayout = new QVBoxLayout();
        diskHeaderTextLayout->setObjectName("diskHeaderTextLayout");
        diskHeaderTitle = new QLabel(mainContentWidget);
        diskHeaderTitle->setObjectName("diskHeaderTitle");
        diskHeaderTitle->setText(QString::fromUtf8("-"));

        diskHeaderTextLayout->addWidget(diskHeaderTitle);

        diskHeaderSubtitle = new QLabel(mainContentWidget);
        diskHeaderSubtitle->setObjectName("diskHeaderSubtitle");
        diskHeaderSubtitle->setText(QString::fromUtf8("-"));

        diskHeaderTextLayout->addWidget(diskHeaderSubtitle);


        diskHeaderLayout->addLayout(diskHeaderTextLayout);

        diskHeaderSpacer = new QSpacerItem(20, 20, QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Minimum);

        diskHeaderLayout->addItem(diskHeaderSpacer);

        diskHeaderCapacityBadge = new QLabel(mainContentWidget);
        diskHeaderCapacityBadge->setObjectName("diskHeaderCapacityBadge");
        diskHeaderCapacityBadge->setText(QString::fromUtf8("-"));

        diskHeaderLayout->addWidget(diskHeaderCapacityBadge);


        m_rightLayout->addLayout(diskHeaderLayout);

        diskHeaderSeparator = new QFrame(mainContentWidget);
        diskHeaderSeparator->setObjectName("diskHeaderSeparator");
        diskHeaderSeparator->setFrameShape(QFrame::HLine);
        diskHeaderSeparator->setFrameShadow(QFrame::Plain);

        m_rightLayout->addWidget(diskHeaderSeparator);

        beforeAfterGridLayout = new QGridLayout();
        beforeAfterGridLayout->setObjectName("beforeAfterGridLayout");
        beforeAfterGridLayout->setVerticalSpacing(0);
        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setSpacing(0);
        verticalLayout_2->setObjectName("verticalLayout_2");
        verticalSpacer_2 = new QSpacerItem(20, 8, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Fixed);

        verticalLayout_2->addItem(verticalSpacer_2);

        m_previewAfterLabel = new QLabel(mainContentWidget);
        m_previewAfterLabel->setObjectName("m_previewAfterLabel");
        m_previewAfterLabel->setText(QString::fromUtf8("After:"));
        m_previewAfterLabel->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignTop);

        verticalLayout_2->addWidget(m_previewAfterLabel);


        beforeAfterGridLayout->addLayout(verticalLayout_2, 2, 0, 1, 1);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(0);
        verticalLayout->setObjectName("verticalLayout");
        verticalSpacer = new QSpacerItem(20, 8, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Fixed);

        verticalLayout->addItem(verticalSpacer);

        m_previewBeforeLabel = new QLabel(mainContentWidget);
        m_previewBeforeLabel->setObjectName("m_previewBeforeLabel");
        m_previewBeforeLabel->setText(QString::fromUtf8("Before:"));
        m_previewBeforeLabel->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignTop);

        verticalLayout->addWidget(m_previewBeforeLabel);


        beforeAfterGridLayout->addLayout(verticalLayout, 0, 0, 1, 1);

        m_previewBeforeFrame = new QWidget(mainContentWidget);
        m_previewBeforeFrame->setObjectName("m_previewBeforeFrame");
        QSizePolicy sizePolicy(QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(m_previewBeforeFrame->sizePolicy().hasHeightForWidth());
        m_previewBeforeFrame->setSizePolicy(sizePolicy);

        beforeAfterGridLayout->addWidget(m_previewBeforeFrame, 0, 1, 1, 1);

        m_previewAfterFrame = new QWidget(mainContentWidget);
        m_previewAfterFrame->setObjectName("m_previewAfterFrame");
        sizePolicy.setHeightForWidth(m_previewAfterFrame->sizePolicy().hasHeightForWidth());
        m_previewAfterFrame->setSizePolicy(sizePolicy);

        beforeAfterGridLayout->addWidget(m_previewAfterFrame, 2, 1, 1, 1);


        m_rightLayout->addLayout(beforeAfterGridLayout);

        diskInfoPanel = new QWidget(mainContentWidget);
        diskInfoPanel->setObjectName("diskInfoPanel");
        diskInfoGrid = new QGridLayout(diskInfoPanel);
        diskInfoGrid->setObjectName("diskInfoGrid");
        diskInfoGrid->setContentsMargins(16, 12, 16, 12);
        diskInfoVSeparator = new QFrame(diskInfoPanel);
        diskInfoVSeparator->setObjectName("diskInfoVSeparator");
        diskInfoVSeparator->setFrameShape(QFrame::VLine);
        diskInfoVSeparator->setFrameShadow(QFrame::Plain);

        diskInfoGrid->addWidget(diskInfoVSeparator, 0, 2, 7, 1);

        label_location = new QLabel(diskInfoPanel);
        label_location->setObjectName("label_location");

        diskInfoGrid->addWidget(label_location, 0, 0, 1, 1);

        locationValueLabel = new QLabel(diskInfoPanel);
        locationValueLabel->setObjectName("locationValueLabel");
        locationValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(locationValueLabel, 0, 1, 1, 1);

        label_capacity = new QLabel(diskInfoPanel);
        label_capacity->setObjectName("label_capacity");

        diskInfoGrid->addWidget(label_capacity, 0, 3, 1, 1);

        capacityValueLabel = new QLabel(diskInfoPanel);
        capacityValueLabel->setObjectName("capacityValueLabel");
        capacityValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(capacityValueLabel, 0, 4, 1, 1);

        diskInfoHSeparator1Left = new QFrame(diskInfoPanel);
        diskInfoHSeparator1Left->setObjectName("diskInfoHSeparator1Left");
        diskInfoHSeparator1Left->setFrameShape(QFrame::HLine);
        diskInfoHSeparator1Left->setFrameShadow(QFrame::Plain);

        diskInfoGrid->addWidget(diskInfoHSeparator1Left, 1, 0, 1, 2);

        diskInfoHSeparator1Right = new QFrame(diskInfoPanel);
        diskInfoHSeparator1Right->setObjectName("diskInfoHSeparator1Right");
        diskInfoHSeparator1Right->setFrameShape(QFrame::HLine);
        diskInfoHSeparator1Right->setFrameShadow(QFrame::Plain);

        diskInfoGrid->addWidget(diskInfoHSeparator1Right, 1, 3, 1, 2);

        label_connection = new QLabel(diskInfoPanel);
        label_connection->setObjectName("label_connection");

        diskInfoGrid->addWidget(label_connection, 2, 0, 1, 1);

        connectionValueLabel = new QLabel(diskInfoPanel);
        connectionValueLabel->setObjectName("connectionValueLabel");
        connectionValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(connectionValueLabel, 2, 1, 1, 1);

        label_child_count = new QLabel(diskInfoPanel);
        label_child_count->setObjectName("label_child_count");

        diskInfoGrid->addWidget(label_child_count, 2, 3, 1, 1);

        childCountValueLabel = new QLabel(diskInfoPanel);
        childCountValueLabel->setObjectName("childCountValueLabel");
        childCountValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(childCountValueLabel, 2, 4, 1, 1);

        diskInfoHSeparator2Left = new QFrame(diskInfoPanel);
        diskInfoHSeparator2Left->setObjectName("diskInfoHSeparator2Left");
        diskInfoHSeparator2Left->setFrameShape(QFrame::HLine);
        diskInfoHSeparator2Left->setFrameShadow(QFrame::Plain);

        diskInfoGrid->addWidget(diskInfoHSeparator2Left, 3, 0, 1, 2);

        diskInfoHSeparator2Right = new QFrame(diskInfoPanel);
        diskInfoHSeparator2Right->setObjectName("diskInfoHSeparator2Right");
        diskInfoHSeparator2Right->setFrameShape(QFrame::HLine);
        diskInfoHSeparator2Right->setFrameShadow(QFrame::Plain);

        diskInfoGrid->addWidget(diskInfoHSeparator2Right, 3, 3, 1, 2);

        label_partition_map = new QLabel(diskInfoPanel);
        label_partition_map->setObjectName("label_partition_map");

        diskInfoGrid->addWidget(label_partition_map, 4, 0, 1, 1);

        partitionMapValueLabel = new QLabel(diskInfoPanel);
        partitionMapValueLabel->setObjectName("partitionMapValueLabel");
        partitionMapValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(partitionMapValueLabel, 4, 1, 1, 1);

        label_type = new QLabel(diskInfoPanel);
        label_type->setObjectName("label_type");

        diskInfoGrid->addWidget(label_type, 4, 3, 1, 1);

        typeValueLabel = new QLabel(diskInfoPanel);
        typeValueLabel->setObjectName("typeValueLabel");
        typeValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(typeValueLabel, 4, 4, 1, 1);

        diskInfoHSeparator3Left = new QFrame(diskInfoPanel);
        diskInfoHSeparator3Left->setObjectName("diskInfoHSeparator3Left");
        diskInfoHSeparator3Left->setFrameShape(QFrame::HLine);
        diskInfoHSeparator3Left->setFrameShadow(QFrame::Plain);

        diskInfoGrid->addWidget(diskInfoHSeparator3Left, 5, 0, 1, 2);

        diskInfoHSeparator3Right = new QFrame(diskInfoPanel);
        diskInfoHSeparator3Right->setObjectName("diskInfoHSeparator3Right");
        diskInfoHSeparator3Right->setFrameShape(QFrame::HLine);
        diskInfoHSeparator3Right->setFrameShadow(QFrame::Plain);

        diskInfoGrid->addWidget(diskInfoHSeparator3Right, 5, 3, 1, 2);

        label_smart = new QLabel(diskInfoPanel);
        label_smart->setObjectName("label_smart");

        diskInfoGrid->addWidget(label_smart, 6, 0, 1, 1);

        smartValueLabel = new QLabel(diskInfoPanel);
        smartValueLabel->setObjectName("smartValueLabel");
        smartValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(smartValueLabel, 6, 1, 1, 1);

        label_device = new QLabel(diskInfoPanel);
        label_device->setObjectName("label_device");

        diskInfoGrid->addWidget(label_device, 6, 3, 1, 1);

        deviceValueLabel = new QLabel(diskInfoPanel);
        deviceValueLabel->setObjectName("deviceValueLabel");
        deviceValueLabel->setText(QString::fromUtf8("-"));

        diskInfoGrid->addWidget(deviceValueLabel, 6, 4, 1, 1);


        m_rightLayout->addWidget(diskInfoPanel);

        rightLayoutTrailingSpacer = new QSpacerItem(20, 20, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Expanding);

        m_rightLayout->addItem(rightLayoutTrailingSpacer);

        m_rightLayout->setStretch(10, 1);

        m_mainLayout->addLayout(m_rightLayout);

        m_mainLayout->setStretch(2, 1);

        m_outerLayout->addWidget(mainContentWidget);


        retranslateUi(ChoicePage);

        QMetaObject::connectSlotsByName(ChoicePage);
    } // setupUi

    void retranslateUi(QWidget *ChoicePage)
    {
        viewMenuButton->setText(QCoreApplication::translate("ChoicePage", "View", nullptr));
        label_location->setText(QCoreApplication::translate("ChoicePage", "Location:", nullptr));
        label_capacity->setText(QCoreApplication::translate("ChoicePage", "Capacity:", nullptr));
        label_connection->setText(QCoreApplication::translate("ChoicePage", "Connection:", nullptr));
        label_child_count->setText(QCoreApplication::translate("ChoicePage", "Child Count:", nullptr));
        label_partition_map->setText(QCoreApplication::translate("ChoicePage", "Partition Map:", nullptr));
        label_type->setText(QCoreApplication::translate("ChoicePage", "Type:", nullptr));
        label_smart->setText(QCoreApplication::translate("ChoicePage", "S.M.A.R.T. Status:", nullptr));
        label_device->setText(QCoreApplication::translate("ChoicePage", "Device:", nullptr));
        (void)ChoicePage;
    } // retranslateUi

};

namespace Ui {
    class ChoicePage: public Ui_ChoicePage {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CHOICEPAGE_H
