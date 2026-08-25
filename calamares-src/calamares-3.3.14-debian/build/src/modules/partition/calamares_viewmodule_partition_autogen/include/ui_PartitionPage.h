/********************************************************************************
** Form generated from reading UI file 'PartitionPage.ui'
**
** Created by: Qt User Interface Compiler version 6.11.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PARTITIONPAGE_H
#define UI_PARTITIONPAGE_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QTreeView>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include <gui/PartitionBarsView.h>
#include <gui/PartitionLabelsView.h>

QT_BEGIN_NAMESPACE

class Ui_PartitionPage
{
public:
    QVBoxLayout *verticalLayout;
    QSplitter *mainSplitter;
    QWidget *sidebarPanel;
    QVBoxLayout *sidebarPanelLayout;
    QTreeView *deviceSidebarView;
    QWidget *detailPanel;
    QVBoxLayout *detailPanelLayout;
    QHBoxLayout *toolbarLayout;
    QToolButton *viewMenuButton;
    QPushButton *newPartitionTableButton;
    QPushButton *createButton;
    QPushButton *editButton;
    QPushButton *deleteButton;
    QSpacerItem *horizontalSpacer_toolbar;
    QPushButton *revertButton;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label_2;
    QComboBox *deviceComboBox;
    QSpacerItem *horizontalSpacer_2;
    PartitionBarsView *partitionBarsView;
    PartitionLabelsView *partitionLabelsView;
    QTreeView *partitionTreeView;
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
    QWidget *lvmButtonPanel;
    QHBoxLayout *lvmButtonLayout;
    QPushButton *newVolumeGroupButton;
    QPushButton *resizeVolumeGroupButton;
    QPushButton *deactivateVolumeGroupButton;
    QPushButton *removeVolumeGroupButton;
    QSpacerItem *verticalSpacer;
    QHBoxLayout *horizontalLayout_3;
    QLabel *label_3;
    QComboBox *bootLoaderComboBox;
    QSpacerItem *horizontalSpacer_3;

    void setupUi(QWidget *PartitionPage)
    {
        if (PartitionPage->objectName().isEmpty())
            PartitionPage->setObjectName("PartitionPage");
        PartitionPage->resize(684, 327);
        PartitionPage->setWindowTitle(QString::fromUtf8("Form"));
        verticalLayout = new QVBoxLayout(PartitionPage);
        verticalLayout->setObjectName("verticalLayout");
        mainSplitter = new QSplitter(PartitionPage);
        mainSplitter->setObjectName("mainSplitter");
        mainSplitter->setOrientation(Qt::Horizontal);
        sidebarPanel = new QWidget(mainSplitter);
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

        mainSplitter->addWidget(sidebarPanel);
        detailPanel = new QWidget(mainSplitter);
        detailPanel->setObjectName("detailPanel");
        detailPanelLayout = new QVBoxLayout(detailPanel);
        detailPanelLayout->setObjectName("detailPanelLayout");
        toolbarLayout = new QHBoxLayout();
        toolbarLayout->setSpacing(8);
        toolbarLayout->setObjectName("toolbarLayout");
        viewMenuButton = new QToolButton(detailPanel);
        viewMenuButton->setObjectName("viewMenuButton");
        viewMenuButton->setPopupMode(QToolButton::InstantPopup);
        viewMenuButton->setToolButtonStyle(Qt::ToolButtonTextOnly);

        toolbarLayout->addWidget(viewMenuButton);

        newPartitionTableButton = new QPushButton(detailPanel);
        newPartitionTableButton->setObjectName("newPartitionTableButton");

        toolbarLayout->addWidget(newPartitionTableButton);

        createButton = new QPushButton(detailPanel);
        createButton->setObjectName("createButton");

        toolbarLayout->addWidget(createButton);

        editButton = new QPushButton(detailPanel);
        editButton->setObjectName("editButton");

        toolbarLayout->addWidget(editButton);

        deleteButton = new QPushButton(detailPanel);
        deleteButton->setObjectName("deleteButton");

        toolbarLayout->addWidget(deleteButton);

        horizontalSpacer_toolbar = new QSpacerItem(40, 20, QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Minimum);

        toolbarLayout->addItem(horizontalSpacer_toolbar);

        revertButton = new QPushButton(detailPanel);
        revertButton->setObjectName("revertButton");
        revertButton->setEnabled(false);

        toolbarLayout->addWidget(revertButton);


        detailPanelLayout->addLayout(toolbarLayout);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        label_2 = new QLabel(detailPanel);
        label_2->setObjectName("label_2");

        horizontalLayout_2->addWidget(label_2);

        deviceComboBox = new QComboBox(detailPanel);
        deviceComboBox->setObjectName("deviceComboBox");

        horizontalLayout_2->addWidget(deviceComboBox);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_2);


        detailPanelLayout->addLayout(horizontalLayout_2);

        partitionBarsView = new PartitionBarsView(detailPanel);
        partitionBarsView->setObjectName("partitionBarsView");

        detailPanelLayout->addWidget(partitionBarsView);

        partitionLabelsView = new PartitionLabelsView(detailPanel);
        partitionLabelsView->setObjectName("partitionLabelsView");

        detailPanelLayout->addWidget(partitionLabelsView);

        partitionTreeView = new QTreeView(detailPanel);
        partitionTreeView->setObjectName("partitionTreeView");
        partitionTreeView->setEditTriggers(QAbstractItemView::NoEditTriggers);
        partitionTreeView->setRootIsDecorated(false);
        partitionTreeView->setAllColumnsShowFocus(true);
        partitionTreeView->setExpandsOnDoubleClick(false);
        partitionTreeView->header()->setStretchLastSection(false);

        detailPanelLayout->addWidget(partitionTreeView);

        diskInfoPanel = new QWidget(detailPanel);
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


        detailPanelLayout->addWidget(diskInfoPanel);

        lvmButtonPanel = new QWidget(detailPanel);
        lvmButtonPanel->setObjectName("lvmButtonPanel");
        lvmButtonLayout = new QHBoxLayout(lvmButtonPanel);
        lvmButtonLayout->setObjectName("lvmButtonLayout");
        newVolumeGroupButton = new QPushButton(lvmButtonPanel);
        newVolumeGroupButton->setObjectName("newVolumeGroupButton");

        lvmButtonLayout->addWidget(newVolumeGroupButton);

        resizeVolumeGroupButton = new QPushButton(lvmButtonPanel);
        resizeVolumeGroupButton->setObjectName("resizeVolumeGroupButton");

        lvmButtonLayout->addWidget(resizeVolumeGroupButton);

        deactivateVolumeGroupButton = new QPushButton(lvmButtonPanel);
        deactivateVolumeGroupButton->setObjectName("deactivateVolumeGroupButton");

        lvmButtonLayout->addWidget(deactivateVolumeGroupButton);

        removeVolumeGroupButton = new QPushButton(lvmButtonPanel);
        removeVolumeGroupButton->setObjectName("removeVolumeGroupButton");

        lvmButtonLayout->addWidget(removeVolumeGroupButton);


        detailPanelLayout->addWidget(lvmButtonPanel);

        verticalSpacer = new QSpacerItem(20, 24, QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Fixed);

        detailPanelLayout->addItem(verticalSpacer);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName("horizontalLayout_3");
        label_3 = new QLabel(detailPanel);
        label_3->setObjectName("label_3");

        horizontalLayout_3->addWidget(label_3);

        bootLoaderComboBox = new QComboBox(detailPanel);
        bootLoaderComboBox->setObjectName("bootLoaderComboBox");
        bootLoaderComboBox->setSizeAdjustPolicy(QComboBox::AdjustToContents);

        horizontalLayout_3->addWidget(bootLoaderComboBox);

        horizontalSpacer_3 = new QSpacerItem(40, 1, QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_3);


        detailPanelLayout->addLayout(horizontalLayout_3);

        mainSplitter->addWidget(detailPanel);

        verticalLayout->addWidget(mainSplitter);

#if QT_CONFIG(shortcut)
        label_2->setBuddy(deviceComboBox);
        label_3->setBuddy(bootLoaderComboBox);
#endif // QT_CONFIG(shortcut)
        QWidget::setTabOrder(deviceSidebarView, deviceComboBox);
        QWidget::setTabOrder(deviceComboBox, revertButton);
        QWidget::setTabOrder(revertButton, partitionTreeView);
        QWidget::setTabOrder(partitionTreeView, newPartitionTableButton);
        QWidget::setTabOrder(newPartitionTableButton, createButton);
        QWidget::setTabOrder(createButton, editButton);
        QWidget::setTabOrder(editButton, deleteButton);
        QWidget::setTabOrder(deleteButton, bootLoaderComboBox);

        retranslateUi(PartitionPage);

        QMetaObject::connectSlotsByName(PartitionPage);
    } // setupUi

    void retranslateUi(QWidget *PartitionPage)
    {
        viewMenuButton->setText(QCoreApplication::translate("PartitionPage", "View", nullptr));
        newPartitionTableButton->setText(QCoreApplication::translate("PartitionPage", "New Partition &Table", nullptr));
        createButton->setText(QCoreApplication::translate("PartitionPage", "Cre&ate", nullptr));
        editButton->setText(QCoreApplication::translate("PartitionPage", "&Edit", nullptr));
        deleteButton->setText(QCoreApplication::translate("PartitionPage", "&Delete", nullptr));
        revertButton->setText(QCoreApplication::translate("PartitionPage", "&Revert All Changes", nullptr));
        label_2->setText(QCoreApplication::translate("PartitionPage", "Storage de&vice:", nullptr));
        label_location->setText(QCoreApplication::translate("PartitionPage", "Location:", nullptr));
        label_capacity->setText(QCoreApplication::translate("PartitionPage", "Capacity:", nullptr));
        label_connection->setText(QCoreApplication::translate("PartitionPage", "Connection:", nullptr));
        label_child_count->setText(QCoreApplication::translate("PartitionPage", "Child Count:", nullptr));
        label_partition_map->setText(QCoreApplication::translate("PartitionPage", "Partition Map:", nullptr));
        label_type->setText(QCoreApplication::translate("PartitionPage", "Type:", nullptr));
        label_smart->setText(QCoreApplication::translate("PartitionPage", "S.M.A.R.T. Status:", nullptr));
        label_device->setText(QCoreApplication::translate("PartitionPage", "Device:", nullptr));
        newVolumeGroupButton->setText(QCoreApplication::translate("PartitionPage", "New Volume Group", nullptr));
        resizeVolumeGroupButton->setText(QCoreApplication::translate("PartitionPage", "Resize Volume Group", nullptr));
        deactivateVolumeGroupButton->setText(QCoreApplication::translate("PartitionPage", "Deactivate Volume Group", nullptr));
        removeVolumeGroupButton->setText(QCoreApplication::translate("PartitionPage", "Remove Volume Group", nullptr));
        label_3->setText(QCoreApplication::translate("PartitionPage", "I&nstall boot loader on:", nullptr));
        (void)PartitionPage;
    } // retranslateUi

};

namespace Ui {
    class PartitionPage: public Ui_PartitionPage {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PARTITIONPAGE_H
