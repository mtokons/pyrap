'''
Created on Oct 3, 2015

@author: nyga
'''
import os

from pyrap.locations import js_loc, code_base

clientjs_files = '''
debug-settings.js
rwt.js
rwt/runtime/BrowserFixes.js
rwt/util/Arrays.js
rwt/util/Objects.js
rwt/util/Strings.js
rwt/util/Numbers.js
rwt/util/Functions.js
rwt/util/Colors.js
rwt/util/Variant.js
rwt/client/Client.js
rwt/qx/Class.js
rwt/qx/Mixin.js
rwt/qx/LegacyProperty.js
rwt/qx/Property.js
rwt/qx/Object.js
rwt/html/Viewport.js
rwt/qx/Target.js
rwt/event/Event.js
rwt/event/DataEvent.js
rwt/event/ChangeEvent.js
rwt/client/Timer.js
rwt/html/Entity.js
rwt/runtime/Singletons.js
rwt/event/EventHandlerUtil.js
rwt/remote/HandlerRegistry.js
rwt/remote/ObjectRegistry.js
rwt/remote/HandlerUtil.js
rwt/util/Encoding.js
rwt/widgets/Display.js
rwt/remote/handler/DisplayHandler.js
rwt/widgets/util/OverStateMixin.js
rwt/widgets/util/HtmlAttributesMixin.js
rwt/widgets/util/WidgetUtil.js
rwt/html/Style.js
rwt/html/Scroll.js
rwt/html/StyleSheet.js
rwt/util/RWTQuery.js
rwt/widgets/base/Widget.js
rwt/widgets/util/WidgetRenderAdapter.js
rwt/widgets/util/Badges.js
rwt/animation/AnimationRenderer.js
rwt/animation/Animation.js
rwt/animation/AnimationUtil.js
rwt/animation/VisibilityAnimationMixin.js
rwt/widgets/base/Parent.js
rwt/event/FocusEvent.js
rwt/event/EventHandler.js
rwt/html/Nodes.js
rwt/event/DomEvent.js
rwt/event/KeyEvent.js
rwt/event/MouseEvent.js
rwt/util/ObjectManager.js
rwt/widgets/util/IframeManager.js
rwt/widgets/CoolBar.js
rwt/remote/handler/CoolBarHandler.js
rwt/widgets/util/LayoutImpl.js
rwt/widgets/util/CanvasLayoutImpl.js
rwt/widgets/base/ClientDocument.js
rwt/widgets/base/Terminator.js
rwt/widgets/base/ClientDocumentBlocker.js
rwt/theme/AppearanceManager.js
rwt/html/Border.js
rwt/html/Font.js
rwt/widgets/util/FocusHandler.js
rwt/html/Location.js
rwt/html/Style.js
rwt/html/Overflow.js
rwt/html/ImageManager.js
rwt/html/Offset.js
rwt/html/ScrollIntoView.js
rwt/widgets/base/BoxLayout.js
rwt/widgets/util/VerticalBoxLayoutImpl.js
rwt/widgets/util/HorizontalBoxLayoutImpl.js
rwt/remote/handler/LabelHandler.js
rwt/widgets/base/Label.js
rwt/widgets/base/Image.js
rwt/html/ImagePreloaderManager.js
rwt/html/ImagePreloader.js
rwt/widgets/util/Layout.js
rwt/widgets/base/HorizontalBoxLayout.js
rwt/widgets/base/Spinner.js
rwt/widgets/base/BasicText.js
rwt/widgets/base/VerticalBoxLayout.js
rwt/util/Range.js
rwt/widgets/TabFolder.js
rwt/widgets/util/RadioManager.js
rwt/widgets/base/TabFolderBar.js
rwt/widgets/base/TabFolderPane.js
rwt/widgets/base/Popup.js
rwt/widgets/util/PopupManager.js
rwt/widgets/util/SelectionManager.js
rwt/widgets/util/Selection.js
rwt/widgets/util/ScrollBarsActivator.js
rwt/widgets/base/AbstractSlider.js
rwt/widgets/base/ScrollBar.js
rwt/html/ImagePreloaderSystem.js
rwt/html/Iframes.js
rwt/remote/Request.js
rwt/widgets/util/ToolTipManager.js
rwt/client/FileUploader.js
rwt/remote/handler/FileUploaderHandler.js
rwt/client/BrowserNavigation.js
rwt/remote/handler/BrowserNavigationHandler.js
rwt/event/DragAndDropHandler.js
rwt/event/DragEvent.js
rwt/widgets/base/Iframe.js
rwt/widgets/util/MResizable.js
rwt/widgets/base/ResizablePopup.js
rwt/widgets/base/Window.js
rwt/widgets/base/HorizontalSpacer.js
rwt/widgets/util/WindowManager.js
rwt/widgets/MenuItemSeparator.js
rwt/widgets/base/TabFolderPage.js
rwt/runtime/ErrorHandler.js
rwt/widgets/util/CellRendererRegistry.js
rwt/widgets/base/GridRowContainer.js
rwt/widgets/util/GridRowContainerWrapper.js
rwt/widgets/util/GridUtil.js
rwt/widgets/util/GridSynchronizer.js
rwt/widgets/base/GridRow.js
rwt/widgets/Menu.js
rwt/remote/handler/MenuHandler.js
rwt/remote/EventUtil.js
rwt/widgets/util/ToolTipConfig.js
rwt/widgets/base/WidgetToolTip.js
rwt/theme/ThemeStore.js
rwt/remote/handler/ThemeStoreHandler.js
rwt/widgets/base/MultiCellWidget.js
rwt/widgets/TabItem.js
rwt/widgets/ListItem.js
rwt/widgets/util/MenuManager.js
rwt/widgets/MenuItem.js
rwt/remote/handler/MenuItemHandler.js
rwt/widgets/util/RadioButtonUtil.js
rwt/widgets/MenuBar.js
rwt/remote/DNDSupport.js
rwt/widgets/DragSource.js
rwt/widgets/DropTarget.js
rwt/remote/handler/DropTargetHandler.js
rwt/remote/handler/DragSourceHandler.js
rwt/theme/ThemeValues.js
rwt/widgets/Grid.js
rwt/remote/handler/ScrollBarHandler.js
rwt/remote/handler/GridHandler.js
rwt/widgets/GridItem.js
rwt/remote/handler/GridItemHandler.js
rwt/widgets/util/GridDNDFeedback.js
rwt/widgets/util/GridCellToolTipSupport.js
rwt/widgets/base/GridHeader.js
rwt/widgets/GridColumn.js
rwt/widgets/base/GridColumnLabel.js
rwt/remote/handler/GridColumnHandler.js
rwt/remote/handler/GridColumnGroupHandler.js
rwt/widgets/Browser.js
rwt/remote/handler/BrowserHandler.js
rwt/widgets/ExternalBrowser.js
rwt/remote/handler/ExternalBrowserHandler.js
rwt/widgets/util/FontSizeCalculation.js
rwt/remote/handler/TextSizeMeasurementHandler.js
rwt/widgets/Label.js
rwt/widgets/base/BasicButton.js
rwt/widgets/ToolItem.js
rwt/widgets/Group.js
rwt/remote/handler/GroupHandler.js
rwt/widgets/Shell.js
rwt/remote/handler/ShellHandler.js
rwt/widgets/ProgressBar.js
rwt/remote/handler/ProgressBarHandler.js
rwt/widgets/Link.js
rwt/remote/handler/LinkHandler.js
rwt/widgets/base/Scrollable.js
rwt/widgets/ScrolledComposite.js
rwt/remote/handler/ScrolledCompositeHandler.js
rwt/widgets/ToolBar.js
rwt/remote/handler/ToolBarHandler.js
rwt/remote/handler/ToolItemHandler.js
rwt/widgets/Scale.js
rwt/remote/handler/ScaleHandler.js
rwt/widgets/ToolItemSeparator.js
rwt/theme/BorderDefinitions.js
rwt/widgets/Combo.js
rwt/remote/handler/ComboHandler.js
rwt/widgets/util/FocusIndicator.js
rwt/remote/handler/GCHandler.js
rwt/widgets/GC.js
rwt/remote/handler/CompositeHandler.js
rwt/widgets/Composite.js
rwt/widgets/Sash.js
rwt/remote/handler/SashHandler.js
rwt/remote/handler/CanvasHandler.js
rwt/widgets/List.js
rwt/remote/handler/ListHandler.js
rwt/widgets/util/TabUtil.js
rwt/remote/handler/TabFolderHandler.js
rwt/remote/handler/TabItemHandler.js
rwt/widgets/base/Calendar.js
rwt/widgets/CoolItem.js
rwt/remote/handler/CoolItemHandler.js
rwt/widgets/Button.js
rwt/remote/handler/ButtonHandler.js
rwt/widgets/FileUpload.js
rwt/remote/handler/FileUploadHandler.js
rwt/widgets/Slider.js
rwt/remote/handler/SliderHandler.js
rwt/widgets/Spinner.js
rwt/remote/handler/SpinnerHandler.js
rwt/widgets/DateTimeTime.js
rwt/widgets/DateTimeDate.js
rwt/widgets/DateTimeCalendar.js
rwt/remote/handler/DateTimeHandler.js
rwt/widgets/ExpandItem.js
rwt/remote/handler/ExpandItemHandler.js
rwt/widgets/ExpandBar.js
rwt/remote/handler/ExpandBarHandler.js
rwt/widgets/Text.js
rwt/remote/handler/TextHandler.js
rwt/widgets/Separator.js
rwt/remote/handler/SeparatorHandler.js
rwt/widgets/ControlDecorator.js
rwt/remote/handler/ControlDecoratorHandler.js
rwt/runtime/MobileWebkitSupport.js
rwt/widgets/ToolTip.js
rwt/remote/handler/ToolTipHandler.js
rwt/remote/WidgetManager.js
rwt/remote/MessageProcessor.js
rwt/remote/MessageWriter.js
rwt/client/ServerPush.js
rwt/remote/handler/ServerPushHandler.js
rwt/remote/Connection.js
rwt/widgets/CTabItem.js
rwt/remote/handler/CTabItemHandler.js
rwt/widgets/CTabFolder.js
rwt/remote/handler/CTabFolderHandler.js
rwt/remote/RemoteObject.js
rwt/remote/RemoteObjectFactory.js
rwt/remote/KeyEventSupport.js
rwt/client/JavaScriptExecutor.js
rwt/remote/handler/ConnectionMessagesHandler.js
rwt/client/ClientMessages.js
rwt/remote/handler/ClientMessagesHandler.js
rwt/remote/handler/JavaScriptExecutorHandler.js
rwt/client/UrlLauncher.js
rwt/remote/handler/UrlLauncherHandler.js
rwt/client/JavaScriptLoader.js
rwt/client/JavaScriptTagLoader.js
rwt/client/CSSLoader.js
rwt/remote/handler/JavaScriptLoaderHandler.js
rwt/remote/handler/JavaScriptTagLoaderHandler.js
rwt/remote/handler/CSSLoaderHandler.js
rwt/runtime/System.js
rwt/widgets/util/MnemonicHandler.js
rap.js
SWT.js
rwt/scripting/EventBinding.js
rwt/scripting/EventProxy.js
rwt/scripting/FunctionFactory.js
rwt/scripting/CompositeProxy.js
rwt/scripting/Synchronizer.js
rwt/scripting/WidgetProxyFactory.js
rwt/remote/handler/FunctionHandler.js
rwt/widgets/util/Template.js
rwt/widgets/util/TemplateRenderer.js
rwt/widgets/DropDown.js
rwt/widgets/util/DropDownSynchronizer.js
rwt/remote/handler/DropDownHandler.js
rwt/client/CopyToClipboard.js
rwt/remote/handler/CopyToClipboardHandler.js
{code_base}/pyrap/pwt/graph/graph.js
{code_base}/pyrap/pwt/barchart/barchart.js
{code_base}/pyrap/pwt/svg/svg.js
{code_base}/pyrap/pwt/ros3d/ros3d.js
{code_base}/pyrap/pwt/radar/radar.js
{code_base}/pyrap/pwt/radar_smoothed/radar_smoothed.js
{code_base}/pyrap/pwt/tree/tree.js
{code_base}/pyrap/pwt/video/video.js
{code_base}/pyrap/pwt/radialdendrogramm/radialdendrogramm.js
{code_base}/pyrap/pwt/bubblyclusters/bubblyclusters.js
{code_base}/pyrap/pwt/plot/plot.js
{code_base}/pyrap/pwt/heatmap/heatmap.js
{code_base}/pyrap/pwt/radialtree/radialtree.js
appearances.js'''.format(code_base=code_base)


def gen_clientjs():
    jscontent = ''
    files = clientjs_files.split('\n')
    for i, filename in enumerate(files):
        if not filename.strip(): continue
        fullpath = filename if os.path.isabs(filename) else os.path.join(js_loc, filename)
        with open(fullpath) as f:
            jscontent += f.read()
        if i < len(files) - 1: jscontent += '\n'
    return jscontent


if __name__ == '__main__':
    print(gen_clientjs())    