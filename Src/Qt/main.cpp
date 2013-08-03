#include "Qt/mainwindow.h"
#include "Qt/qti.h"

#include <QtCore/QEvent>
#include <QtCore/QWaitCondition>
#include <QtCore/QMutex>
#include <QtCore/QSize>
#include <QtCore/QThread>
#include <QtGui/QApplication>
#include <QtGui/QDesktopWidget>
#include <QtGui/QResizeEvent>
#include <QtGui/QToolTip>
#include <QtGui/QLabel>
#include <QtGui/QDialog>
#include <QtGui/QLayout>
#include <stdio.h>

QMutex canvasupdatemutex(QMutex::Recursive);

extern "C" void vcs_acquire_update() {
  //fprintf(stderr,"mutex lock\n");
   canvasupdatemutex.lock();
}

extern "C" void vcs_release_update() {
  //fprintf(stderr,"mutex unlock\n");
   canvasupdatemutex.unlock();
}

extern "C" void vcs_Qt_window_bell(void)
{
  //fprintf(stderr,"do not forget to put a bell!\n");
  QApplication::beep();
}
extern "C" void vcs_Qt_init_window(PyVCScanvas_Object *vcscanvas)
{
  VCSQtManager::window(vcscanvas->canvas_id)->vcs_obj = vcscanvas;
}

extern "C" void vcs_Qt_open_window_by_id(int i)
{
  VCSQtManager::sendEvent(i, VCS_SHOW_EVENT);
}

extern "C" void vcs_Qt_repaint_window_by_id(int id)
{
  VCSQtManager::sendEvent(id, VCS_REPAINT_EVENT);
}

extern "C" void VCS2CAIRO_setrgb(cairo_t *cr,int color);

extern "C" void vcs_Qt_clear_window_by_id(int id)
{
  MainWindow *window = VCSQtManager::window(id);
  if (window->vcs_obj->connect_id.cr !=NULL) {
    VCS2CAIRO_setrgb(window->vcs_obj->connect_id.cr,0);
    cairo_paint(window->vcs_obj->connect_id.cr);
    vcs_Qt_repaint_window_by_id(id);
  }
  return;
}

extern "C" void vcs_Qt_clear_window_by_id_without_repaint(int id)
{
  MainWindow *window = VCSQtManager::window(id);
  if (window->vcs_obj->connect_id.cr !=NULL) {
    VCS2CAIRO_setrgb(window->vcs_obj->connect_id.cr,0);
    cairo_paint(window->vcs_obj->connect_id.cr);
  }
  return;
}

// extern "C" void vcs_Qt_close_window(int index)
// {
//   QCoreApplication::postEvent(VCSQtWindows[index], new QEvent(VCS_HIDE_EVENT));
//   return;
// }
// extern "C" void vcs_Qt_animation_created(int index){
//   QVCSEvent *event = new QVCSEvent(VCS_ANIMATION_CREATED_EVENT);
//   VCSQtManager::sendEvent(index, event);
// }

extern "C" void vcs_Qt_resize_window(int index,int x,int y,int w, int h)
{
  QVCSEvent *event = new QVCSEvent(VCS_RESIZE_EVENT);
  event->geom.setX(x);
  event->geom.setY(y);
  event->geom.setWidth(w);
  event->geom.setHeight(h);
  VCSQtManager::sendEvent(index, event);
}
extern "C" void vcs_Qt_window_set_cursor_by_id(int index, QCursor cursor)
{
  VCSQtManager::window(index)->setCursor(cursor);
}
extern "C" void vcs_Qt_destroy_window(int index)
{
  /* First make sure we kill any cairo existing at this point */
  vcs_acquire_update();
  vcs_release_update();
  QCoreApplication::postEvent(VCSQtManager::window(index), new QEvent(VCS_HIDE_EVENT));
}
extern "C" void vcs_Qt_set_window_properties(int index, int minWidth, int minHeight, int maxWidth,int maxHeight, char *icon, char *title)
{
  QVCSEvent *event = new QVCSEvent(VCS_PROP_EVENT);
  event->minWidth = minWidth;
  event->minHeight = minHeight;
  event->maxWidth = maxWidth;
  event->maxHeight = maxHeight;
  if (icon!=NULL) {
    strcpy(event->icon,icon);
  }
  if (title!=NULL) {
    strcpy(event->title,title);
  }
  VCSQtManager::sendEvent(index, event);
}

extern "C" void vcs_Qt_display_info(int id, Gpoint pointA, struct data_point info)
{
  QVCSEvent *event = new QVCSEvent(VCS_INFO_EVENT);
  event->info = info;
  event->point = pointA;
  VCSQtManager::sendEvent(id, event);
}

extern "C" void vcs_Qt_display_menu(int id, float x, float y)
{
  QToolTip::showText(QCursor::pos(), "Hello World");
  QVCSEvent *event = new QVCSEvent(VCS_MENU_EVENT);
  event->point.x = x;
  event->point.y = y;
  VCSQtManager::sendEvent(id, event);
}

extern "C" void vcs_Qt_hide_info(int id)
{
  VCSQtManager::sendEvent(id, VCS_HIDE_INFO_EVENT);
}

extern "C" void vcs_Qt_get_window_visibility_by_id(int id,int *visibility)
{
  *visibility = (int) VCSQtManager::window(id)->isVisible();
}

extern "C" void vcs_Qt_get_window_dimensions_by_id(int id,int *x, int *y,int *w,int *h)
{
  QRect geom = VCSQtManager::window(id)->geometry();
  *x= geom.x();
  *y= geom.y();
  *w= geom.width();
  *h= geom.height();
}

extern "C" void vcs_Qt_get_desktop_dimensions(int index,int *x, int *y, int *w,int *h)
{
  QDesktopWidget *mydesktop = QApplication::desktop();
  QRect geom = mydesktop->screenGeometry(VCSQtManager::window(index));
  *x= geom.x();
  *y= geom.y();
  *w= geom.width();
  *h= geom.height();
}

extern "C" void vcs_Qt_window_get_image_by_id(int id, void **ximage)
{
  MainWindow *window = VCSQtManager::window(id);
  size_t num2 = cairo_image_surface_get_stride(window->vcs_obj->connect_id.surface)*cairo_image_surface_get_height (window->vcs_obj->connect_id.surface);
  *ximage = malloc(num2);
  unsigned char *beg = cairo_image_surface_get_data (window->vcs_obj->connect_id.surface);
  memcpy(*ximage,beg,num2);
}

extern "C" void vcs_Qt_window_put_image_by_id(int id, void *ximage)
{
  QVCSEvent *event = new QVCSEvent(VCS_PUT_IMAGE_EVENT, true);
  fprintf(stderr,"Yeah got in created event, id is: %i\n",id);
  fprintf(stderr,"data are at: %p\n",ximage);
  event->data = ximage;
  VCSQtManager::sendEvent(id, event);
}

extern "C" void vcs_Qt_window_put_qimage_by_id(int id, QImage *qImage)
{
  QVCSEvent *event = new QVCSEvent(VCS_PUT_QIMAGE_EVENT, true);
  event->data = (void*)qImage;
  VCSQtManager::sendEvent(id, event);
}

extern "C" void vcs_Qt_put_image_from_png_file(int id, char *fnm) {
    void *image;
    fprintf(stderr,"ok we received id and file: %i, %s\n",id,fnm);
    vcs_Qt_window_put_qimage_by_id(id, new QImage(fnm));
    // QImage img0(fnm);
    // fprintf(stderr,"ok readin :%i \n",img0.format());
    // QImage img = img0.convertToFormat(QImage::Format_ARGB32_Premultiplied);
    // fprintf(stderr,"ok converted to: %i\n",img.format());
    // QSize sz = img.size();
    // fprintf(stderr,"Size is: %ix%i\n",sz.width(),sz.height());
    // image = malloc(sz.width()*sz.height()*4);
    // memcpy(image,img.bits(),sz.width()*sz.height()*4);
    // vcs_Qt_window_put_image_by_id(id,image);
}

extern "C" void vcs_Qt_image_create(void **image, int width, int height)
{
  QImage img(width,height,QImage::Format_ARGB32_Premultiplied);
  img.fill(Qt::white);
  *image = malloc(width*height*4);
  memcpy(*image,img.bits(),width*height*4);
}

extern "C" void vcs_Qt_image_get_pixel(void *image,int width,int height, int i, int j, unsigned long *pixel)
{
  QImage img((uchar *)image,width,height,QImage::Format_ARGB32_Premultiplied);
  QRgb pix = img.pixel(i,j);
  *pixel = pix;
}

extern "C" void vcs_Qt_image_put_pixel(void **image, int width, int height, int i, int j , unsigned long pixel)
{
  QImage img((uchar *)*image,width,height,QImage::Format_ARGB32_Premultiplied);
  img.setPixel(i,j,pixel);
}

static void setAppIcon() {
  char *base_dir, dirbase[1024], icon_file[1024];
  if ((base_dir=getenv("PCMDI_GRAPHICS_DIR")) == NULL) {
    base_dir = getenv("HOME");
    if ((base_dir) == NULL || strlen(base_dir) ==0)
      strcpy(dirbase,"./PCMDI_GRAPHICS");
    else {
      strcpy(dirbase,base_dir);
      strcat(dirbase,"/PCMDI_GRAPHICS");
    }
  } else 
    strcpy(dirbase,base_dir);
  base_dir=dirbase;
  strcpy(icon_file, base_dir);
  strcat(icon_file, "/vcs_icon.xbm");
  VCSQtManager::app()->setWindowIcon(QIcon(icon_file));
}

static QMutex createdMutex;

extern "C" void createVCSCanvases()
{
  createdMutex.lock();
  if (!VCSQtManager::isCreated()) { // only run the the app once
    if (!VCSQtManager::app()) {
      static int argc = 1;
      static char *argv[]= {"null"};
      static QPythonApp *app = new QPythonApp(argc, argv);
    }
    VCSQtManager::createCanvases();
    if (VCSQtManager::owningApp())
      VCSQtManager::executeDeferred(setAppIcon);
  }
  createdMutex.unlock();
}
