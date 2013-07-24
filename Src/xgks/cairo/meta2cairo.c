/*
*
*  This software was developed by the Thermal Modeling and Analysis
*  Project(TMAP) of the National Oceanographic and Atmospheric
*  Administration's (NOAA) Pacific Marine Environmental Lab(PMEL),
*  hereafter referred to as NOAA/PMEL/TMAP.
*
*  Access and use of this software shall impose the following
*  obligations and understandings on the user. The user is granted the
*  right, without any fee or cost, to use, copy, modify, alter, enhance
*  and distribute this software, and any derivative works thereof, and
*  its supporting documentation for any purpose whatsoever, provided
*  that this entire notice appears in all copies of the software,
*  derivative works and supporting documentation.  Further, the user
*  agrees to credit NOAA/PMEL/TMAP in any publications that result from
*  the use of this software or in any product that includes this
*  software. The names TMAP, NOAA and/or PMEL, however, may not be used
*  in any advertising or publicity to endorse or promote any products
*  or commercial entity unless specific written permission is obtained
*  from NOAA/PMEL/TMAP. The user also understands that NOAA/PMEL/TMAP
*  is not obligated to provide the user with any support, consulting,
*  training or assistance of any kind with regard to the use, operation
*  and performance of this software nor to provide the user with any
*  updates, revisions, new versions or "bug fixes".
*
*  THIS SOFTWARE IS PROVIDED BY NOAA/PMEL/TMAP "AS IS" AND ANY EXPRESS
*  OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
*  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
*  ARE DISCLAIMED. IN NO EVENT SHALL NOAA/PMEL/TMAP BE LIABLE FOR ANY SPECIAL,
*  INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
*  RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
*  CONTRACT, NEGLIGENCE OR OTHER TORTUOUS ACTION, ARISING OUT OF OR IN
*  CONNECTION WITH THE ACCESS, USE OR PERFORMANCE OF THIS SOFTWARE.  
*
*/



/*
 * PostScript driver for XGKS metafiles
 * Created by Joe Sirott, Pacific Marine Environmental Lab
 *
 */

/*
 *		Copyright IBM Corporation 1989
 *
 *                      All Rights Reserved
 *
 * Permission to use, copy, modify, and distribute this software and its
 * documentation for any purpose and without fee is hereby granted,
 * provided that the above copyright notice appear in all copies and that
 * both that copyright notice and this permission notice appear in
 * supporting documentation, and that the name of IBM not be
 * used in advertising or publicity pertaining to distribution of the
 * software without specific, written prior permission.
 *
 * IBM DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
 * ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
 * IBM BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
 * ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
 * WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
 * ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
 * SOFTWARE.
 *
 *
 * University of Illinois at Urbana-Champaign
 * Department of Computer Science
 * 1304 W. Springfield Ave.
 * Urbana, IL	61801
 *
 * (C) Copyright 1987, 1988 by The University of Illinois Board of Trustees.
 * All rights reserved.
 *
 * Tool: X 11 Graphical Kernel System
 * Author: Gregory Scott Rogers
 * Author: Sung Hsien Ching Kelvin
 * Author: Yu Pan
 */

/*LINTLIBRARY*/

#define NULL 0
#include <stdarg.h>
#include <wchar.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>		/* for time(), localtime(), and strftime() */
#include <sys/types.h>		/* for uid_t */
#include <sys/utsname.h>	/* for uname() */
#include <unistd.h>		/* for getlogin() */
#include <string.h>
#include <ctype.h>
#include <assert.h>
#include <stdarg.h>
#include <wchar.h>
#ifdef USEX11
#include "udposix.h"
#else
typedef void    *voidp;
#endif
#include "gks_implem.h"
#include "cgm.h"		/* for public, API details */
#include "cgm_implem.h"		/* for implementation details */
#include "ps.h"
#include <cairo/cairo.h>
#include <cairo/cairo-ps.h>
#include <cairo/cairo-ft.h>
#include <cairo/cairo-features.h>
#include <cairo/cairo-pdf.h>
#include <cairo/cairo-ps.h>
#include <cairo/cairo-svg.h>
#include <cairo/cairo-xlib.h>

/*#include <cairo/cairo-xlib-xrender.h>*/


#ifndef lint
    static char afsid[]	= "$__Header$";
    static char rcsid[]	= "$Id$";
#endif

static char MARKERSIZE[] = "markersize";
static char LINEWIDTHSCALE[] = "lws";
static char CHAREXPANSION[] = "charexpansion";
static char CHARSPACING[] = "charspacing";
static char LINECOLOR[] = "lc";
static char MARKERCOLOR[] = "mc";
static char FILLCOLOR[] = "fc";
static char TEXTCOLOR[] = "tc";
static char header[] = 
#include "headerv4.0.h"
;
static Gint	postscript_version = 1;

/* 11 bytes dummy for this implementation */
static Gchar	dummy[] = "dummy info.";

/* String array for formats created on the fly */
static Gchar	fmt[80];

static Gtxalign CAIROalign;
static Gpoint CAIROup, CAIRObase;

static Gflinter FillStyle = GHOLLOW;

/* VCS defs */
#include "gks.h"
#include "gksshort.h"
#ifdef USEX11
#include <X11/Xlib.h>
#endif
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include "color.h"
#include "workstations.h"

extern Gconid_X_drawable connect_id; /* VCS canvas drawable id */
extern struct color_table C_tab;
extern struct c_val 		std_color[16];
extern char active_colors[17];
extern struct orientation       Page;

/* Error messages are switched on and off through the environment */
/* variable XGKS_LOG anded with the enum MsgLog */

typedef enum MsgLog {
  INFO = 1,
  WARN = 2,
  ERR = 4
} MsgLog;

 int LogFlag = ERR;

 void initLogFlag()
{
  char *cp = getenv("XGKS_LOG");
  if (cp){
    LogFlag = atoi(cp);
  }
}

int pattern_index;

extern char text_hpath,text_vpath,text_path;
extern float text_height,text_angle;
extern int text_color,text_font;

/* Charles Doutriaux Stream write func for cairo*/

cairo_status_t stream_cairo_write (void	 *closure,
	    const unsigned char	*data,
	    unsigned int	 length)
{
  FILE	*fp = closure;
  int i;
/*   char tmp[]; */
/*   strncpy(tmp,data,length); */
/*   tmp[length-1]='\0'; */
/*   printf("length is: %i\n",length); */
/*   printf("data: %s\n",tmp); */
  for(i=0;i<length;i++){
    fputc( data[i],fp);
  }
  return CAIRO_STATUS_SUCCESS;
};

static void msgInfo(char *format, ...)
{
  if (LogFlag & INFO){
    va_list ap;
    va_start(ap, format);
    /* print out name of function causing error */
    fprintf(stderr, "XGKS(CAIRO): Info: ");
    /* print out remainder of message */
    vfprintf(stderr, format, ap);
    va_end(ap);
  }
}

static void msgWarn(char *format, ...)
{
  va_list ap;
  va_start(ap, format);
  //printf( format, ap); 
  if (LogFlag & WARN){
    va_start(ap, format);
    /* print out name of function causing error */
    fprintf(stderr, "XGKS(CAIRO): Warning: ");
    /* print out remainder of message */
    vfprintf(stderr, format, ap);
    va_end(ap);
  }
}

static void msgErr(char *format, ...)
{
  if (LogFlag & ERR){
    va_list ap;
    va_start(ap, format);
    /* print out name of function causing error */
    fprintf(stderr, "XGKS(CAIRO): Error: ");
    /* print out remainder of message */
    vfprintf(stderr, format, ap);
    va_end(ap);
  }
}


static void set_lineStyle(mf_cgmo *cgmo, Gint attr, Gasf type)
{
  if (type != xgks_state.gks_lnattr.type)
    return;
  if (type == GBUNDLED){
    attr = cgmo->ws->lnbundl_table[attr].type;
  }
  double dashes[4];
  int ndashes,i;
  msgInfo("set_lineStyle: setting style to %d\n", attr);
  switch(attr){
  case 1:
    ndashes=0;
    dashes[0]=1.;
    dashes[1]=0.;
    break;
  case 2:
    ndashes=2;
    dashes[0]=8.;
    dashes[1]=8.;
    break;
  case 3:
    ndashes=2;
    dashes[0]=4.;
    dashes[1]=4.;
    break;
  case 4:
    ndashes=4;
    dashes[0]=8.;
    dashes[1]=4.;
    dashes[2]=4.;
    dashes[3]=4.;
    break;
  case -3:
    ndashes=2;
    dashes[0]=16.;
    dashes[1]=16.;
    break;
  default:
    ndashes=1;
    dashes[0]=1.;
    break;
  }
  extern int YW;
  for (i=0;i<ndashes;i++) dashes[i]=dashes[i]*(float)YW/792.;
  cairo_set_dash(cgmo->ws->cr,dashes,ndashes,0.);
#ifdef GENCAIRO
  printf("ndashes=%i;\n",ndashes);
  for (i=0;i<ndashes;i++) printf("dashes[%i]=%i;\n",i,dashes[i]);
  printf("cairo_set_dash(cr,dashes,ndashes,0.);\n");
#endif

}

static void
set_lineWidth(mf_cgmo *cgmo, double size, Gint attr, Gasf type)
{
  if (type != xgks_state.gks_lnattr.width)
    return;
  if (type == GBUNDLED){
    size = cgmo->ws->lnbundl_table[attr].width;
  }
  msgInfo("set_lineWidth: setting width to %lf\n", size);
  extern int YW;
  cairo_set_line_width(cgmo->ws->cr,(int)size*(float)YW/792.*.5);
  //cairo_set_line_width(cgmo->ws->cr,1.);
#ifdef GENCAIRO
  printf("cairo_set_line_width(cr,%f*(float)%i/792.*.5);\n",size,YW);
#endif

/*   if (size < 1.0) */
/*     size = 1.0; */
/*   size *= 0.5; */
/*   fprintf(cgmo->fp, "/%s %.6lf def\n", LINEWIDTHSCALE, size); */
}

static void set_lineColor(mf_cgmo *cgmo, Gint attr, Gasf type)
{
  if (type != xgks_state.gks_lnattr.colour)
    return;
  if (type == GBUNDLED){
    attr = cgmo->ws->lnbundl_table[attr].colour;
  }
  msgInfo("set_lineColor: setting color index to %d\n", attr);
  VCS2CAIRO_setrgb(cgmo->ws->cr,attr);
/*   fprintf(cgmo->fp, "/%s %d def\n", LINECOLOR, attr); */
  
}


/*
 * Return a string identifying the user and installation.
 */
    static Gchar*
XgksMAuthor(void)
{
    char		*username	= getlogin();
    struct utsname	name;
    static Gchar	buffer[41];

    buffer[0]	= 0;

    if (username != NULL)
	(void) strncat(buffer, username, sizeof(buffer) - 1);

    if (uname(&name) != -1) {
	int	nchr	= strlen(buffer);

	if (nchr < sizeof(buffer) - 1) {
	    buffer[nchr++]	= '@';
	    (void) strncpy(buffer + nchr, name.nodename, 
			   sizeof(buffer) - nchr - 1);
	}
    }

    return buffer;
}


/*
 * Return a date-string.
 */
    static Gchar*
XgksMDate(void)
{
    time_t          clock = time((time_t *) NULL);
    static Gchar    date[9];

    (void) strftime(date, (size_t)sizeof(date), "%y/%m/%d", 
                    localtime(&clock));

    return date;
}

/*
 * Set the clear flag in an output PostScript file.
 */
    int
CAIROclear(Metafile *mf, int num, Gclrflag flag)
{
  cairo_surface_t *surface=NULL;;
#ifdef GENCAIRO
  printf("cairo_destroy(cr);\ncr = NULL;\ncr = cairo_create(surface);\n");
#endif
  surface = cairo_get_target(mf->cgmo->ws->cr);
  cairo_destroy(mf->cgmo->ws->cr);
  mf->cgmo->ws->cr = cairo_create(surface);
/*   if (mf != NULL && mf->cgmo != NULL) { */
/*     mf_cgmo *cgmo	= mf->cgmo; */
/*     FILE *fp = cgmo->fp; */
/*     if (fp != NULL){ */
/*       fprintf(fp, "gr gs clippath 1 setgray fill\n"); */
/*     } */
/*   } */
  return OK;
}


/*
 * Redraw all segments in an output PostScript file.
 */
    int
CAIROredrawAllSeg(Metafile **mf, int num)
{
				/* Noop */
  msgWarn("CAIROredrawAllSeg: Don't support this feature\n");
  return OK;
}


/*
 * Set the update flag in an output PostScript file.
 */
     int
CAIROupdate(Metafile **mf, int num, Gregen regenflag)
{
				/* Noop */
  msgWarn("CAIROupdate: Don't support this feature\n");
  return OK;
}


/*
 * Set the deferal state in an output PostScript file.
 */
    int
CAIROdefer(Metafile **mf, int num, Gdefmode defer_mode, Girgmode regen_mode)
{
				/* Noop */
  msgWarn("CAIROdefer: Don't support this feature\n");
  return OK;
}


extern Gpoint VCS2PSDEVICE();


Gpoint VCS2DEVICE(cairo_t *cr, double x,double y)
{
  extern int XW ;
  extern int YW ;
  Gpoint to;
  double xr,yr,x2,y2;

  /* if (cairo_surface_get_type(cairo_get_target(cr))==CAIRO_SURFACE_TYPE_PS) {ç */
  /*   //to = VCS2PSDEVICE(x,y); */
  /*   //x2=to.x; */
  /*   //y2=to.y; */
  /*   cairo_user_to_device (cr, &x, &y); */
  /*   x2=(int)x; */
  /*   y2=(int)y; */
  /*   to.x=x2; */
  /*   to.y=y2; */

  /* } */
  /* else { */
  {
    if (strcmp(Page.page_orient,"landscape")==0) {
      xr=1.;
      /* yr=1.3195884995223088; */
      yr = (float)XW/(float)YW;
      //printf("xr: %f, yr: %f\n",xr,yr);
    }
    else {
      /* xr=1.3195884995223088; */
      yr=1.;
      xr = (float)YW/(float)XW;
    }
    x2 = x*xr*XW;
    y2 = YW - y*yr*YW;
    cairo_user_to_device (cr, &x2, &y2);
    x2=(int)x2;
    y2=(int)y2;
    to.x=x2;
    to.y=y2;
  }
  return to;
}
void VCS2DEVICE_moveto(cairo_t *cr, double x,double y)
{
  double dx,dy;
  Gpoint to;
  to = VCS2DEVICE(cr,x,y);
  dx = to.x;
  dy = to.y;
  cairo_move_to(cr,dx,dy);
#ifdef GENCAIRO
  printf("cairo_move_to(cr,%f,%f);\n",dx,dy);
#endif
}
void VCS2DEVICE_lineto(cairo_t *cr, double x,double y)
{
  double dx,dy;
  Gpoint to;
  to = VCS2DEVICE(cr,x,y);
  dx = to.x;
  dy = to.y;
  cairo_line_to(cr,dx,dy);
#ifdef GENCAIRO
  printf("cairo_line_to(cr,%f,%f);\n",dx,dy);
#endif
}
/*
 * Write text to an output  file.
 * Charles Doutriaux Version to plug in cairo stuff
 */
    int
CAIROtext(Metafile *mf, int num, Gpoint *at, Gchar *string)
{
  double dx,dy;
  int imf;
  
  if (cairo_get_target(mf->cgmo->ws->cr)==NULL) {
    return OK;
  }
  VCS2DEVICE_moveto(mf->cgmo->ws->cr,(double)at->x,(double)at->y);
  for (imf = 0; imf < num; ++imf) {  
    
    VCS2CAIRO_drawString(at,string,mf->cgmo->ws->cr);
  }
 return OK;
 /* #endif /\* #if 0 *\/ */
}
/*
 * Write a cell array to an output PostScript file.
 * New method fakes transparency by not writing image data for colors of 0
 */

    int
CAIROcellArray(Metafile *mf, int num, Gpoint *ll, Gpoint *ur, Gpoint *lr, Gint row, Gint *colour, Gipoint *dim)
{
  msgWarn("CAIROcellArray: Don't support this feature\n");
  return OK;
}


/*
 * Close a segment in an output PostScript file.
 */
    int
CAIROcloseSeg(Metafile *mf, int num)
{
				/* Noop */
  msgWarn("CAIROcloseSeg: Don't support this feature\n");
  return OK;
}


/*
 * Set the graphic attributes in an output PostScript file.
 */

/*
 * Write a graphic to output PostScript files.
 *
 * This routine is suitable for
 *
 *	POLYLINE    -- code == 11
 *	POLYMARKER  -- code == 12
 *	FILLAREA    -- code == 14
 */
/* Charles Doutriaux added support for xgks patterns and hatches */
/* RETURN HERE ****************/

cairo_t *prep_image_surface(cr,w,h,style)
     int w,h,style;
     cairo_t *cr;
{
    cairo_surface_t *image=NULL;
    cairo_t *cr2=NULL;
    cairo_pattern_t *pattern=NULL;
/* 	if (image!=NULL) { */
/* 	  cairo_surface_destroy(image); */
/* #ifdef GENCAIRO */
/* 	  printf("cairo_surface_destroy(image);\n"); */
/* #endif	 */
/* 	} */
    image = cairo_surface_create_similar(cairo_get_target(cr),CAIRO_CONTENT_COLOR_ALPHA,w,h);
#ifdef GENCAIRO
    printf("image = cairo_surface_create_similar(surface,CAIRO_CONTENT_COLOR_ALPHA,%i,%i);\n",w,h);
#endif
    /* 	if (cr2!=NULL) { */
    /* 	  cairo_destroy(cr2); */
    /* #ifdef GENCAIRO */
    /* 	  printf("cairo_destroy(cr2);\n"); */
    /* #endif	 */
    /* 	} */
    cr2 = cairo_create (image);
#ifdef GENCAIRO
    printf("cr2 = cairo_create (image);\n");
#endif	
    if (style==1) { /* style = 1 means pattern colored */
      pattern = cairo_get_source(cr);
      cairo_set_source(cr2,pattern);
#ifdef GENCAIRO
      printf("pattern = cairo_get_source(cr);\n");
      printf("cairo_set_source(cr2,pattern);\n");
#endif
      /* 	  cairo_set_miter_limit(cr2,0.); */
    }
    return cr2;
}

cairo_pattern_t *CAIROcreatePattern(cr,index,style)
     cairo_t *cr;
     int index,style;
{
  cairo_pattern_t *pattern=NULL;
  cairo_matrix_t matrix;
  cairo_t *cr2=NULL;
  switch (index) {
  case 1:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_move_to(cr2,0,0);
    cairo_line_to(cr2,0,3);
    cairo_line_to(cr2,3,3);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_move_to(cr2,0,0);\n");
    printf("cairo_line_to(cr2,0,3);\n");
    printf("cairo_line_to(cr2,3,3);\n");
    printf("cairo_fill(cr2);\n");
#endif	
    break;
  case 2:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_rectangle(cr2,0,2,2,2);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,2,2,2);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 3:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_move_to(cr2,0,0);
    cairo_line_to(cr2,2,0);
    cairo_line_to(cr2,2,2);
    cairo_line_to(cr2,4,2);
    cairo_line_to(cr2,4,4);
    cairo_line_to(cr2,0,4);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_move_to(cr2,0,0);\n");
    printf("cairo_line_to(cr2,2,0);\n");
    printf("cairo_line_to(cr2,2,2);\n");
    printf("cairo_line_to(cr2,4,2);\n");
    printf("cairo_line_to(cr2,4,4);\n");
    printf("cairo_line_to(cr2,0,4);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 4:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_rectangle(cr2,0,0,2,2);
    cairo_rectangle(cr2,2,2,2,2);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,2,2);\n");
    printf("cairo_rectangle(cr2,2,2,2,2);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 5:
    cr2=prep_image_surface(cr,1,4,style);
    cairo_rectangle(cr2,0,0.5,1,2.5);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0.5,1,2.5);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 6:
    cr2=prep_image_surface(cr,4,1,style);
    cairo_rectangle(cr2,0,0,3,1);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,3,1);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 7:
    cr2=prep_image_surface(cr,1,4,style);
    cairo_rectangle(cr2,0,0,1,1);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,1,1);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 8:
    cr2=prep_image_surface(cr,4,1,style);
    cairo_rectangle(cr2,0,0,1,1);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,1,1);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 9:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_set_line_width(cr2,1);
    cairo_move_to(cr2,4,0);
    cairo_line_to(cr2,0,4);
    cairo_stroke(cr2);
    cairo_move_to(cr2,4,-4);
    cairo_line_to(cr2,-4,4);
    cairo_stroke(cr2);
    cairo_move_to(cr2,8,0);
    cairo_line_to(cr2,0,8);
    cairo_stroke(cr2);
#ifdef GENCAIRO
    printf("cairo_set_line_width(cr2,1);\n");
    printf("cairo_move_to(cr2,4,0);\n");
    printf("cairo_line_to(cr2,0,4);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,4,-4);\n");
    printf("cairo_line_to(cr2,-4,4);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,8,0);\n");
    printf("cairo_line_to(cr2,0,8);\n");
    printf("cairo_stroke(cr2);\n");
#endif
    break;
  case 10:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_set_line_width(cr2,2);
    cairo_move_to(cr2,4,0);
    cairo_line_to(cr2,0,4);
    cairo_stroke(cr2);
    cairo_move_to(cr2,4,-4);
    cairo_line_to(cr2,-4,4);
    cairo_stroke(cr2);
    cairo_move_to(cr2,8,0);
    cairo_line_to(cr2,0,8);
    cairo_stroke(cr2);
#ifdef GENCAIRO
    printf("cairo_set_line_width(cr2,2);\n");
    printf("cairo_move_to(cr2,4,0);\n");
    printf("cairo_line_to(cr2,0,4);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,4,-4);\n");
    printf("cairo_line_to(cr2,-4,4);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,8,0);\n");
    printf("cairo_line_to(cr2,0,8);\n");
    printf("cairo_stroke(cr2);\n");
#endif
    break;
  case 11:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_set_line_width(cr2,1);
    cairo_move_to(cr2,0,0);
    cairo_line_to(cr2,4,4);
    cairo_stroke(cr2);
    cairo_move_to(cr2,-4,0);
    cairo_line_to(cr2,4,8);
    cairo_stroke(cr2);
    cairo_move_to(cr2,0,-4);
    cairo_line_to(cr2,8,4);
    cairo_stroke(cr2);
#ifdef GENCAIRO
    printf("cairo_set_line_width(cr2,1);\n");
    printf("cairo_move_to(cr2,0,0);\n");
    printf("cairo_line_to(cr2,4,4);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,-4,0);\n");
    printf("cairo_line_to(cr2,4,8);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,0,-4);\n");
    printf("cairo_line_to(cr2,8,4);\n");
    printf("cairo_stroke(cr2);\n");
#endif
    break;
  case 12:
    cr2=prep_image_surface(cr,4,4,style);
    cairo_set_line_width(cr2,2);
    cairo_move_to(cr2,0,0);
    cairo_line_to(cr2,4,4);
    cairo_stroke(cr2);
    cairo_move_to(cr2,-4,0);
    cairo_line_to(cr2,4,8);
    cairo_stroke(cr2);
    cairo_move_to(cr2,0,-4);
    cairo_line_to(cr2,8,4);
    cairo_stroke(cr2);
#ifdef GENCAIRO
    printf("cairo_set_line_width(cr2,2);\n");
    printf("cairo_move_to(cr2,0,0);\n");
    printf("cairo_line_to(cr2,4,4);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,-4,0);\n");
    printf("cairo_line_to(cr2,4,8);\n");
    printf("cairo_stroke(cr2);\n");
    printf("cairo_move_to(cr2,0,-4);\n");
    printf("cairo_line_to(cr2,8,4);\n");
    printf("cairo_stroke(cr2);\n");
#endif
    break;
  case 13:
    cr2=prep_image_surface(cr,7,7,style);
    cairo_rectangle(cr2,0,0,6,6);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,6,6);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 14:
    cr2=prep_image_surface(cr,7,7,style);
    cairo_rectangle(cr2,0,0,6,6);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,6,6);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
/*   case 14: */
/*     cr2=prep_image_surface(cr,7,7,style); */
/*     cairo_move_to(cr2,0,3.5); */
/*     cairo_line_to(cr2,3.5,0); */
/*     cairo_line_to(cr2,7,3.5); */
/*     cairo_line_to(cr2,3.5,7); */
/*     cairo_fill(cr2); */
/*     break; */
  case 15:
    cr2=prep_image_surface(cr,8,1,style);
    cairo_rectangle(cr2,0,0,2,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,3,0,4,1);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,2,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,3,0,4,1);\n");
    printf("cairo_fill(cr2);\n");
#endif
   break;
  case 16:
    cr2=prep_image_surface(cr,1,8,style);
    cairo_rectangle(cr2,0,0,1,2);
    cairo_fill(cr2);
    cairo_rectangle(cr2,0,3,1,4);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,1,2);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,0,3,1,4);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 17:
    cr2=prep_image_surface(cr,8,8,style);
    cairo_rectangle(cr2,0,0,1,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,4,0,1,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,0,4,1,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,4,4,1,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,1,1,3,3);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,5,3,3);
    cairo_fill(cr2);
    cairo_rectangle(cr2,1,5,2,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,1,2,1);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,1,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,4,0,1,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,0,4,1,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,4,4,1,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,1,1,3,3);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,5,3,3);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,1,5,2,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,1,2,1);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 18:
    cr2=prep_image_surface(cr,8,5,style);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,8,0);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,-16,0);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,0,5);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,8,0);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,8,0);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,0,-10);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,-8,0);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
    cairo_translate(cr2,-8,0);
    cairo_rectangle(cr2,0,1,4,1.5);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,0,2,4);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,8,0);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,-16,0);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,0,5);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,8,0);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,8,0);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,0,-10);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,-8,0);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_translate(cr2,-8,0);\n");
    printf("cairo_rectangle(cr2,0,1,4,1.5);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,0,2,4);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 19:
    cr2=prep_image_surface(cr,8,8,style);
    cairo_rectangle(cr2,1,0,7,2);
    cairo_fill(cr2);
    cairo_rectangle(cr2,0,2,1,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,2,2,5,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,0,3,2,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,7,3,1,4);
    cairo_fill(cr2);
    cairo_rectangle(cr2,0,4,4,2);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,4,2,2);
    cairo_fill(cr2);
    cairo_rectangle(cr2,0,6,3,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,4,6,1,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,6,6,2,1);
    cairo_fill(cr2);
    cairo_rectangle(cr2,3,7,3,1);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,1,0,7,2);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,0,2,1,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,2,2,5,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,0,3,2,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,7,3,1,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,0,4,4,2);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,4,2,2);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,0,6,3,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,4,6,1,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,6,6,2,1);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,3,7,3,1);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  case 20:
    cr2=prep_image_surface(cr,9,10,style);
    //fprintf(stderr,"CAIRO STATUS cr2: %s]\n",cairo_status_to_string(cairo_status(cr2)));
    cairo_rectangle(cr2,0,0,8,4);
    //fprintf(stderr,"CAIRO STATUS2 cr2: %s\n",cairo_status_to_string(cairo_status(cr2)));
    cairo_fill(cr2);
    cairo_rectangle(cr2,-4,5,8,4);
    cairo_fill(cr2);
    cairo_rectangle(cr2,5,5,8,4);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,8,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,-4,5,8,4);\n");
    printf("cairo_fill(cr2);\n");
    printf("cairo_rectangle(cr2,5,5,8,4);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  default:
    printf("painting default case %i\n",index);
    cr2=prep_image_surface(cr,1,1,style);
    cairo_rectangle(cr2,0,0,1,1);
    cairo_fill(cr2);
#ifdef GENCAIRO
    printf("cairo_rectangle(cr2,0,0,1,1);\n");
    printf("cairo_fill(cr2);\n");
#endif
    break;
  }

  pattern = cairo_pattern_create_for_surface (cairo_get_target(cr2));
  cairo_pattern_set_extend (pattern, CAIRO_EXTEND_REPEAT);
#ifdef GENCAIRO
  printf("pattern = cairo_pattern_create_for_surface (cairo_get_target(cr2));\n");
  printf("cairo_pattern_set_extend (pattern, CAIRO_EXTEND_REPEAT);\n");
#endif
  if ((index==18) || (index==14)) {
    matrix.xx = 0.707106781187;
    matrix.xy = -0.707106781187;
    matrix.yx = 0.707106781187;
    matrix.yy=0.707106781187;
    matrix.x0=0.;
    matrix.y0=0.;
    cairo_pattern_set_matrix(pattern,&matrix);
#ifdef GENCAIRO
    printf("matrix.xx = 0.707106781187;\n");
    printf("matrix.xy = -0.707106781187;\n");
    printf("matrix.yx = 0.707106781187;\n");
    printf("matrix.yy=0.707106781187;\n");
    printf("matrix.x0=0.;\n");
    printf("matrix.y0=0.;\n");
    printf("cairo_pattern_set_matrix(pattern,&matrix);\n");
#endif
  }
  //fprintf(stderr,"CAIRO STATUS3 cr2: %s\n",cairo_status_to_string(cairo_status(cr2)));
  cairo_destroy(cr2);
  cr2=NULL;
  return pattern; 
}

cairo_t *metafile_cr = NULL;

    int
CAIROoutputGraphic(Metafile *mf, int num, Gint code, Gint num_pt, Gpoint *pos)
{
    int		imf;
    cairo_pattern_t *pattern=NULL;
    extern VCS2CAIRO_setrgb();
    int              w, h,stype;
    mf_cgmo		**cgmo	= &mf->cgmo;
    for (imf = 0; imf < num; ++imf) {
	Gint	i;
	FILE	*fp	= cgmo[imf]->fp;
	assert(num_pt > 0);
	switch(code){
	  case GKSM_FILL_AREA:
	    if ((FillStyle == 2) || (FillStyle == 3)){
	
	      if (FillStyle == 3){ /*hatch */
		pattern = CAIROcreatePattern(mf->cgmo->ws->cr,pattern_index,1);
	      }
	      else {
		pattern = CAIROcreatePattern(mf->cgmo->ws->cr,pattern_index,0);
	      }
	      cairo_set_source(mf->cgmo->ws->cr,pattern);
#ifdef GENCAIRO
	      printf("cairo_set_source(cr,pattern);\n");
#endif
	      VCS2DEVICE_moveto(mf->cgmo->ws->cr,pos->x,pos->y);
/* 	      fprintf(fp, "[/Pattern [/DeviceRGB] ]  setcolorspace\n"); */
/* 	      fprintf(fp, "%s gcol mypattern setcolor %.6f %.6f m\n", FILLCOLOR, pos->x, pos->y); */
	    } else if (FillStyle == 2 ){ //pattern
/* 	      fprintf(fp, "[/Pattern [/DeviceRGB] ]  setcolorspace\n"); */
/* 	      fprintf(fp, "241 gcol mypattern setcolor %.6f %.6f m\n", pos->x, pos->y); */
	    } else { //normal
	      VCS2DEVICE_moveto(mf->cgmo->ws->cr,pos->x,pos->y);
	    }
	    break;
	  case GKSM_POLYLINE:
/* 	    VCS2CAIRO_setrgb(cr,LINECOLOR); */
	    VCS2DEVICE_moveto(mf->cgmo->ws->cr,pos->x,pos->y);
	    break;
	  case GKSM_POLYMARKER:
/* 	    fprintf(fp, "%s o %.6f %.6f pm\n", MARKERCOLOR, pos->x, pos->y); */
/* 	    VCS2DEVICE_moveto(pos->x,pos->y); */
/* 	      VCS2CAIRO_setrgb(cr,MARKERCOLOR); */
/* 	      VCS2DEVICE_moveto(pos->x,pos->y); */
/* 	      VCS2CAIRO_drawMarker(cr,1); //??? need to pass marker type! ??? */
	    break;
	  default:
	    fprintf(stderr, "CAIROoutputGraphics: Unknown code %d\n", code);
	    return OK;
	}
	{
	  Gpoint *npos = pos;
	  npos++;
	  for (i = 1; i < num_pt; ++i,++npos) {
	    if (code == GKSM_POLYMARKER) {
/* 	      VCS2DEVICE_moveto(pos->x,pos->y); */
/* 	      VCS2CAIRO_drawMarker(cr,1); //??? need to pass marker type! ??? */
	    }
	    else 
	      VCS2DEVICE_lineto(mf->cgmo->ws->cr,npos->x,npos->y);
	  }
	}
	switch(code){
	  case GKSM_FILL_AREA:
	    if (FillStyle == GHOLLOW){
/* 	      fprintf(fp, "%s\n", LineStyles[1]); */
/* 	      fprintf(fp, "%.6f %.6f l\n", pos->x, pos->y); */
/* 	      fprintf(fp, "t\n"); */
	      VCS2DEVICE_lineto(mf->cgmo->ws->cr,pos->x,pos->y);
	      cairo_close_path(mf->cgmo->ws->cr);
	      cairo_stroke(mf->cgmo->ws->cr);
#ifdef GENCAIRO
	      printf("cairo_close_path(cr);\n");
	      printf("cairo_stroke(cr);\n");
#endif
	    } else {
/* 	      cairo_close_path(cr); */
	      //cairo_set_fill_rule(mf->cgmo->ws->cr,CAIRO_FILL_RULE_EVEN_ODD);
	      //cairo_set_antialias(mf->cgmo->ws->cr,CAIRO_ANTIALIAS_NONE);
	      cairo_close_path(mf->cgmo->ws->cr);
	      /* Need this to avoid white lines in postscript */
	      stype = cairo_surface_get_type(cairo_get_target(mf->cgmo->ws->cr));
	      if ((stype==CAIRO_SURFACE_TYPE_PS) || (stype==CAIRO_SURFACE_TYPE_PDF)) {
		cairo_set_line_width(mf->cgmo->ws->cr,1.);
		cairo_stroke_preserve(mf->cgmo->ws->cr);
#ifdef GENCAIRO
		printf("cairo_set_line_width(cr,1.);\n");
		printf("cairo_stroke_preserve(cr);\n");
#endif
	      }
	      cairo_fill(mf->cgmo->ws->cr);
#ifdef GENCAIRO
	      printf("cairo_fill(cr);\n");
#endif
	    }
	    break;
	  case GKSM_POLYMARKER:
	      cairo_fill(mf->cgmo->ws->cr);
#ifdef GENCAIRO
	      printf("cairo_fill(cr);\n");
#endif
	    break;
	  case GKSM_POLYLINE:
	    cairo_stroke(mf->cgmo->ws->cr);
#ifdef GENCAIRO
	      printf("cairo_stroke(cr);\n");
#endif
/* 	    fprintf(fp, "t\n"); */
	    break;
	}
    }
    return OK;
}
/*
 * Set the size of graphics in an output PostScript file.
 */
    int
CAIROsetGraphSize(Metafile *mf, int num, Gint code, double size)
{
    int imf;
    mf_cgmo		**cgmo	= &mf->cgmo;

    for (imf = 0; imf < num; ++imf) {
      switch(code){
      case GKSM_LINEWIDTH_SCALE_FACTOR:
	set_lineWidth(cgmo[imf], size, 0, GINDIVIDUAL);
	break;
      case GKSM_CHARACTER_EXPANSION_FACTOR:
      case GKSM_MARKER_SIZE_SCALE_FACTOR:
      case GKSM_CHARACTER_SPACING:
	msgWarn("CAIROsetGraphSize: Don't support code %d\n", code);
	break;
      default:
	msgWarn("CAIROsetGraphSize: Unknown code %d\n", code);
      }
    }
    return OK;
}



int
CAIROsetGraphAttr(Metafile *mf, int num, Gint code, Gint attr)
{
    int		imf;
    mf_cgmo		**cgmo	= &mf->cgmo;
    char *comm = 0;
    for (imf = 0; imf < num; ++imf) {
      switch(code){
      case GKSM_POLYLINE_INDEX:
	set_lineStyle(cgmo[imf], attr, GBUNDLED);
	set_lineColor(cgmo[imf], attr, GBUNDLED);
	set_lineWidth(cgmo[imf], 0.0, attr, GBUNDLED);
	break;
      case GKSM_POLYLINE_COLOUR_INDEX:
	set_lineColor(cgmo[imf], attr, GINDIVIDUAL);
	break;
      case GKSM_LINETYPE:
	set_lineStyle(cgmo[imf], attr, GINDIVIDUAL);
	break;
      case GKSM_POLYMARKER_COLOUR_INDEX:
	comm = MARKERCOLOR;
	break;
      case GKSM_TEXT_COLOUR_INDEX:
	text_color = attr;
	break;
      case GKSM_FILL_AREA_COLOUR_INDEX:
	VCS2CAIRO_setrgb(mf->cgmo->ws->cr,attr);
	break;
      case GKSM_MARKER_TYPE:
      case GKSM_POLYMARKER_INDEX:
      case GKSM_FILL_AREA_INDEX:
	break;
      case GKSM_FILL_AREA_STYLE_INDEX:
	pattern_index = attr;

	break;
      case GKSM_PICK_IDENTIFIER:
      case GKSM_TEXT_INDEX:
	msgWarn("CAIROsetGraphAttr: Don't support code %d\n", code);
	/* Ignore */
	break;
      default:
	msgWarn("CAIROsetGraphAttr: Unknown code %d\n", code);
      }

    }
    return OK;
}


/*
 * Set the font precision in an output PostScript file.
 */
    int
CAIROsetTextFP(Metafile *mf, int num, Gtxfp *txfp)
{
    if (!txfp)
      return OK;
    text_font=txfp->font;
    msgWarn("CAIROsetTextFp: Don't support this feature\n");
    return OK;
}

#define HYPOT(x,y) sqrt((double)((x)*(x) + (y)*(y)))


/*
 * Set the character up-vector and character height in an output PostScript file.
 */
    int
CAIROsetCharUp(Metafile *mf, int num, Gpoint *up, Gpoint *base)
{
  double angle;
    if (up == 0 || base == 0)
      return OK;
    if ((up->y<0.0000001)&&(-.0000001<up->y)) angle = 90.*sign(up->x)*sign(up->y);
  else angle = atan(up->x/up->y)/3.1415926536*180.;
  text_height = HYPOT(up->x,up->y);
  if (sign(up->y)==1) {
    text_angle=-angle;
  }
  else {
    text_angle=180-angle;
  }
    msgWarn("CAIROsetCharUp: Don't support this feature\n");
    return OK;
/* #if 1 */
/*     float height; */
/*     int imf; */
/*     mf_cgmo		**cgmo	= &mf->cgmo; */
/*     if (up == 0 || base == 0) */
/*       return OK; */

/*     CAIROup = *up; */
/*     CAIRObase = *base; */
/*     height = HYPOT(up->x, up->y); */

/*     for (imf = 0; imf < num; ++imf) { */
/* 	FILE	*fp	= cgmo[imf]->fp; */
/* 	fprintf(fp, "%.6f sf\n", height); */
/*     } */

/* #ifdef CAIRODEBUG */
/*     fprintf(stderr, "CAIROsetCharUp: up=(%.6f %.6f) base=(%.6f %.6f) height = %.6f\n", */
/* 	    up->x, up->y, */
/* 	    base->x, base->y, height); */
/* #endif */
/*     return OK; */
/* #endif /\* #if 0 *\/ */
}


/*
 * Set the text-path in an output PostScript file.
 */
    int
CAIROsetTextPath(Metafile *mf, int num, Gtxpath path)
{

  //msgWarn("CAIROsetTextPath: Don't support this feature\n");
  switch(path) {
  case     GTP_RIGHT:
    text_path = 'r';
    break;
  case     GTP_LEFT:
    text_path = 'l';
    break;
  case    GTP_UP:
    text_path = 'u';
    break;
  case GTP_DOWN:
    text_path='d';
    break;
  }

    return OK;
}


/*
 * Set the text-alignment in an output PostScript file.
 */
    int
CAIROsetTextAlign(Metafile *mf, int num, Gtxalign *align)
{
  //msgWarn("CAIROsetTextAlign: Don't support this feature\n");
  switch(align->hor) {
  case GTH_LEFT:
    text_hpath = 'l';
    break;
  case GTH_CENTRE:
    text_hpath='c';
    break;
  case GTH_RIGHT:
    text_hpath='r';
  default:
    text_hpath='r';
  }
  switch(align->ver){
  case GTV_TOP:
    text_vpath='t';
    break;
  case GTV_CAP:
    text_vpath='c';
    break;
  case GTV_HALF:
    text_vpath='h';
    break;
  case GTV_BASE:
    text_vpath='b';
    break;
  case GTV_BOTTOM:
    text_vpath='s';
    break;
  default:
    text_vpath='h';
    break;
  }
    return OK;
/* /\* #if 0 *\/ */
/*     if (align == 0) */
/*       return; */
/*     CAIROalign = *align; */
/* #ifdef CAIRODEBUG */
/*     fprintf(stderr, "CAIROsetTextAlign: align = %d %d\n", align->hor, align->ver); */
/* #endif */
/*     return OK; */
/* /\* #endif /\\* #if 0 *\\/ *\/ */
}


/*
 * Set the interior fill-style in an output PostScript file.
 */
    int
CAIROsetFillStyle(Metafile *mf, int num, Gflinter style)
{
  FillStyle = style;
  return OK;
}


/*
 * Set the pattern size in an output PostScript file.
 */
    int
CAIROsetPatSize(Metafile *mf, int num)
{
    msgWarn("CAIROsetPatSize: Don't support this feature\n");
    return OK;
}


/*
 * Set the pattern reference-point in an output PostScript file.
 */
    int
CAIROsetPatRefpt(Metafile *mf, int num)
{
    msgWarn("CAIROsetPatRefpt: Don't support this feature\n");
    return OK;
}


/*
 * Set the ASF in an output PostScript file.
 */
    int
CAIROsetAsf(Metafile *mf, int num)
{
    msgWarn("CAIROsetAsf: Don't support this feature\n");
    return OK;
}


/*
 * Set the line and marker representation in an output PostScript file.
 */
    int
CAIROsetLineMarkRep(Metafile *mf, int num, Gint code, Gint idx, Gint type, double size, Gint colour)
{
    msgWarn("CAIROsetLineMarkRep: Don't support this feature\n");
    return OK;
}


/*
 * Set the text representation in an output PostScript file.
 */
    int
CAIROsetTextRep(Metafile *mf, int num, Gint idx, Gtxbundl *rep)
{
  printf("text rep\n");
/*     msgWarn("CAIROsetTextRep: Don't support this feature\n"); */
/*     return OK; */
/* #if 0 */
    if (!rep)
      return 0;
#ifdef CAIRODEBUG
    fprintf(stderr, "CAIROsetTextRep: index %d font prec (%d %d) exp %.6f sp %.6f color %d\n",
	    idx, rep->fp.font, rep->fp.prec,
	    rep->ch_exp, rep->space, rep->colour);
#endif
    return OK;
/* #endif */
}


/*
 * Set the fill representation in an output PostScript file.  
 */
    int
CAIROsetFillRep(Metafile *mf, int num, Gint idx, Gflbundl *rep)
{
    msgWarn("CAIROsetFillRep: Don't support this feature\n");
    return OK;
}


/*
 * Set the pattern representation in an output PostScript file.
 */
    int
CAIROsetPatRep(Metafile *mf, int num, Gint idx, Gptbundl *rep)
{
    msgWarn("CAIROsetPatRep: Don't support this feature\n");
    return OK;
}


/*
 * Set the colour representation in an output PostScript file.
 * Also write out gray scale version
 */
#ifndef MAX
#define MAX(a,b)    (((a)>(b))?(a):(b))
#endif

    int
CAIROsetColRep(Metafile *mf, int num, Gint idx, Gcobundl *rep)
{
    int		imf;
    mf_cgmo		**cgmo	= &mf->cgmo;
    msgWarn("CAIROsetColRep: Don't support this feature\n");
    return OK;
/*     for (imf = 0; imf < num; ++imf) { */
/* 	FILE	*fp	= cgmo[imf]->fp; */
/* 	float r = rep->red, g = rep->green, b = rep->blue; */
/* 	allocate_color(cgmo[imf], idx, r, g, b); */
/*     } */

/*     return OK; */
}


/*
 * Set the clipping rectangle in an output PostScript file.
 * Note that an unpaired grestore
 * is used to restore the initial clipping path before setting up the
 * clip; this means that no other unpaired gsaves may be used.
 */
    int
CAIROsetClip(Metafile *mf, int num, Glimit *rect)
{
  Gpoint tmp,tmp2;
  tmp = VCS2DEVICE(mf->cgmo->ws->cr,rect->xmin,rect->ymin);
  tmp2 = VCS2DEVICE(mf->cgmo->ws->cr,rect->xmax,rect->ymax);

    cairo_restore(mf->cgmo->ws->cr);
    cairo_save(mf->cgmo->ws->cr);
    cairo_rectangle(mf->cgmo->ws->cr,tmp.x,tmp.y,tmp2.x-tmp.x,tmp2.y-tmp.y);
    cairo_clip(mf->cgmo->ws->cr);
#ifdef GENCAIRO
    printf("cairo_restore(cr);\n");
    printf("cairo_save(cr);\n");
    printf("cairo_rectangle(cr,%f,%f,%f,%f);\n",tmp.x,tmp.y,tmp2.x-tmp.x,tmp2.y-tmp.y);
    printf("cairo_clip(cr);\n");
#endif
    return OK;
}


/*
 * Set the viewport limits in an output PostScript file.
 */
    int
CAIROsetLimit(Metafile *mf, int num, Gint code, Glimit *rect)
{
    msgWarn("CAIROsetLimit: Don't support this feature\n");
    return OK;
}


/*
 * Rename a segment in an output PostScript file.
 */
    int
CAIROrenameSeg(Metafile *mf, int num, Gint old, Gint new)
{
    msgWarn("CAIROrenameSeg: Don't support this feature\n");
    return OK;
}


/*
 * Set the segment transformation in an output PostScript file.
 */
    int
CAIROsetSegTran(Metafile *mf, int num, Gint name, Gfloat (*matrix)[])
{
    msgWarn("CAIROsetSegTran: Don't support this feature\n");
    return OK;
}


/*
 * Set the segment attributes in an output PostScript file.
 */
    int
CAIROsetSegAttr(Metafile *mf, int num, Gint name, Gint code, Gint attr)
{
    msgWarn("CAIROSetSegAttr: Don't support this feature\n");
    return OK;
}


/*
 * Set the segment visibility in an output Metafile.
 */
    int
CAIROsetSegVis(Metafile *mf, int num, Gint name, Gsegvis vis)
{
    msgWarn("CAIROsetSegVis: Don't support this feature\n");
    return OK;
}


/*
 * Set segment highlighting in an output PostScript file.
 */
    int
CAIROsetSegHilight(Metafile *mf, int num, Gint name, Gseghi hilight)
{
    msgWarn("CAIROsetSegHiglight: Don't support this feature\n");
    return OK;
}


/*
 * Set segment priority in an output PostScript file.
 */
    int
CAIROsetSegPri(Metafile *mf, int num, Gint name, double pri)
{
    msgWarn("CAIROsetSegPri: Don't support this feature\n");
    return OK;
}


/*
 * Set segment detectability in an output PostScript file.
 */
    int
CAIROsetSegDetect(Metafile *mf, int num, Gint name, Gsegdet det)
{
    msgWarn("CAIROsetSegDetect: Don't support this feature\n");
    return OK; 
}

/*
 * Close an output PostScript file.
 */
    int
CAIROmoClose(Metafile *mf)
{
  extern void draw_logo(cairo_t *cr);
  cairo_surface_t *surface;
  int status = 1;		/* return status error */
  if (mf != NULL && mf->cgmo != NULL) {
    mf_cgmo *cgmo	= mf->cgmo;
    FILE *fp = cgmo->fp;
    surface = cairo_get_target(cgmo->ws->cr);
    /* draws the logo */
    draw_logo(cgmo->ws->cr);
    if (fp != NULL) {
      cairo_show_page(cgmo->ws->cr);
      /* plug for png output ? */
      if (cairo_surface_get_type(surface)==CAIRO_SURFACE_TYPE_IMAGE) {
	cairo_surface_write_to_png_stream(surface,stream_cairo_write,fp);
      }
      cairo_destroy (cgmo->ws->cr);
      cairo_surface_flush(surface);
      cairo_surface_finish(surface);
      cairo_surface_destroy (surface);
#ifdef GENCAIRO
      printf("cairo_destroy (cr);\n");
      printf("cairo_surface_flush(surface);\n");
      printf("cairo_surface_finish(surface);\n");
      printf("cairo_surface_destroy (surface);\n");
      printf("}\n");
#endif
      if (!ferror(fp) & fclose(fp) != EOF)
	status	= OK;
    }

    ufree((voidp)mf->cgmo);
    mf->cgmo	= NULL;
  }

  return status;
}


/* device dependent Output */

extern char meta_type[5];
/*
 * Write a message to an output PostScript file.
 */
    int
CAIROmessage(Metafile *mf, int num, Gchar *string)
{
  char tmp[256];
  int length;
  cairo_surface_t *surface=NULL;
  surface = cairo_get_target(mf->cgmo->ws->cr);
  length = strlen(string);
  strcpy(tmp,"%");
  strcat(tmp,string);
  if (length>254) tmp[256]='\0';
  else tmp[length+1]='\0';
  if (cairo_surface_get_type(surface)==CAIRO_SURFACE_TYPE_PS) {
    cairo_ps_surface_dsc_comment(surface,tmp);
#ifdef GENCAIRO
    printf("cairo_ps_surface_dsc_comment(surface,\"%s\");\n",tmp);
#endif
  }
  else {
    msgWarn("CAIROmessage: Don't support this feature for this surface type\n");

  }
  return OK;
}

void CAIROresize(WS_STATE_PTR ws, Gpoint size)
{

  cairo_surface_t *surface=NULL;
  surface = cairo_get_target(ws->cr);
  if (cairo_surface_get_type(surface)==CAIRO_SURFACE_TYPE_PS) {
    cairo_ps_surface_set_size(surface,size.x,size.y);
#ifdef GENCAIRO
    printf("cairo_ps_surface_set_size(surface,%i,%i);\n",size.x,size.y);
#endif
  }
  else {
    msgWarn("CAIROresize: Don't support this feature for this surface type\n");

  }
}

/*
 * Open an output PostScript file.
 */
    int
CAIROmoOpen(WS_STATE_PTR ws)
{
  extern int PSmoOpen();
  extern int SVGmoOpen();
  extern int PNGmoOpen();
  extern int PDFmoOpen();
  cairo_t *cr = connect_id.cr;
  if (strcmp(meta_type,"ps")==0) {
    PSmoOpen(ws);
  }
  else if (strcmp(meta_type,"svg")==0) {
    SVGmoOpen(ws);
  }
  else if (strcmp(meta_type,"png")==0) {
    PNGmoOpen(ws);
  }
  else if (strcmp(meta_type,"pdf")==0) {
    PDFmoOpen(ws);
  }
  else {
    msgWarn("CAIROmoOpen: Don't support this feature for this surface type\n");
  }
  cairo_save(ws->cr); /* needed for clipping */
#ifdef GENCAIRO
  printf("cairo_save(cr);\n"); /* needed for clipping */
#endif
/*   printf("opened, surface status: %s\n",cairo_status_to_string(cairo_surface_status(surface))); */
   return OK;
}

