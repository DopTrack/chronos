var creative = {};
var loopTotal;
var descuento = 0;
creative.init = function () {
  creative.setupDOMElements();

  if (Enabler.isInitialized()) {
    creative.enablerInitHandler();
  } else {
    Enabler.addEventListener(
      studio.events.StudioEvent.INIT,
      creative.enablerInitHandler);
  }
};

creative.setupDOMElements = function () {
  creative.domElements = {};
  creative.domElements.background = document.getElementById('background');
   creative.domElements.background2 = document.getElementById('background2');
  creative.domElements.background3 = document.getElementById('background3');
  creative.domElements.ctaUrl = document.getElementById('ctaUrl');
  creative.domElements.txtFrame1 =  document.getElementById('txtFrame1');
  creative.domElements.txtFrame2 =  document.getElementById('txtFrame2');
  creative.domElements.textoFrame2Linea2 =  document.getElementById('textoFrame2Linea2');
  creative.domElements.btnText =  document.getElementById('btnText');
  creative.domElements.capaClick = document.getElementById('capa_click');
};

creative.enablerInitHandler = function (event) {
  creative.dynamicDataAvailable();

  creative.domElements.ctaUrl.addEventListener('click', creative.exitClickHandler);
  creative.domElements.btnText.addEventListener('click', creative.exitClickHandler);
  creative.domElements.capaClick.addEventListener('click', creative.exitClickHandler);

  if (Enabler.isPageLoaded()) {
    creative.pageLoadHandler();
  } else {
    Enabler.addEventListener(
      studio.events.StudioEvent.PAGE_LOADED,
      creative.pageLoadHandler);
  }
};

var dynamicContent = {};
creative.dynamicDataAvailable = function () {
    Enabler.setProfileId(1042943);

    dynamicContent.NH_Hoteles_RTB_2015= [{}];
    dynamicContent.NH_Hoteles_RTB_2015[0]._id = 0;
    dynamicContent.NH_Hoteles_RTB_2015[0].Id = 1;
    dynamicContent.NH_Hoteles_RTB_2015[0].Report_label = "VBN-Default-Belgium";
    dynamicContent.NH_Hoteles_RTB_2015[0].Destination_Id = "";
    dynamicContent.NH_Hoteles_RTB_2015[0].Destino = "";
    dynamicContent.NH_Hoteles_RTB_2015[0].Peso = 100;
    dynamicContent.NH_Hoteles_RTB_2015[0].Default = false;
    dynamicContent.NH_Hoteles_RTB_2015[0].Loop = 2;
    dynamicContent.NH_Hoteles_RTB_2015[0].Imagenes_fondo = {"background_300x600_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36804113/63009_20150527013104174_background_300x600_3.jpg"},"background_300x600_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36804702/63009_20150527013057121_background_300x600_2.jpg"},"background_300x600_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36804026/63009_20150527013049583_background_300x600_1.jpg"},"background_300x250_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36803911/63009_20150527013042103_background_300x250_3.jpg"},"background_300x250_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36804025/63009_20150527013034344_background_300x250_2.jpg"},"background_300x250_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36804701/63009_20150527013026228_background_300x250_1.jpg"},"background_468x60_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36881199/63009_20150603244954132_background_468x60_3.jpg"},"background_468x60_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36884070/63009_20150603244946073_background_468x60_2.jpg"},"background_468x60_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36890719/63009_20150603244937113_background_468x60_1.jpg"},"background_728x90_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36793899/63009_20150527013127164_background_728x90_3.jpg"},"background_728x90_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36800351/63009_20150527013119406_background_728x90_2.jpg"},"background_728x90_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36804703/63009_20150527013112127_background_728x90_1.jpg"},"background_160x600_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36653797/63009_20150513082406443_background_160x600_3.jpg"},"background_160x600_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36654253/63009_20150513082401020_background_160x600_2.jpg"},"background_160x600_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36655009/63009_20150513082355262_background_160x600_1.jpg"},"background_120x600_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36653796/63009_20150513082344111_background_120x600_3.jpg"},"background_120x600_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36654726/63009_20150513082328656_background_120x600_2.jpg"},"background_120x600_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/36653698/63009_20150513082322830_background_120x600_1.jpg"}};
    dynamicContent.NH_Hoteles_RTB_2015[0].Youtube_ID_120x600 = "yeAvzlt8OU4";
    dynamicContent.NH_Hoteles_RTB_2015[0].Youtube_ID_160x600 = "-vdzVifHcFo";
    dynamicContent.NH_Hoteles_RTB_2015[0].Youtube_ID_300x250 = "WqAf1sMWv9c";
    dynamicContent.NH_Hoteles_RTB_2015[0].Youtube_ID_300x600 = "lHNNhr7zai4";
    dynamicContent.NH_Hoteles_RTB_2015[0].Youtube_ID_728x90 = "tmDzcistOMA";
    dynamicContent.NH_Hoteles_RTB_2015[0].Destino_Pais = "";
    dynamicContent.NH_Hoteles_RTB_2015[0].Destino_Ciudad = "";
    dynamicContent.NH_Hoteles_RTB_2015[0].Texto_1 = "Kostenfreies Frühstück<br>Kostenfreier Late Check-out<br>Kinder kostenfrei";
    dynamicContent.NH_Hoteles_RTB_2015[0].Descuento = 0;
    dynamicContent.NH_Hoteles_RTB_2015[0].Texto_2 = "Cet \u00E9t\u00E9 vous serez comme \u00E0 la maison.<br>Mais encore mieux.";
    dynamicContent.NH_Hoteles_RTB_2015[0].cta = "R\u00C9SERVEZ ICI";
    dynamicContent.NH_Hoteles_RTB_2015[0].URL_destino = {};
    dynamicContent.NH_Hoteles_RTB_2015[0].URL_destino.Url = "http://www.nh-hotels.fr?dis=13311&nhagentid=12740&nhsubagentid=127405333311&ct=%eaid!";
    dynamicContent.NH_Hoteles_RTB_2015[0].btn_mas_info = "MORE INFO";
    dynamicContent.NH_Hoteles_RTB_2015[0].Texto_3 = "CONOCE NUESTRA SELECCI\u00D3N DE HOTELES";
    dynamicContent.NH_Hoteles_RTB_2015[0].btn_expand = "EXPAND";
    dynamicContent.NH_Hoteles_RTB_2015[0].Texto_1_Expand = "HOTELS IN <b>BARCELONA<\/b>";
    dynamicContent.NH_Hoteles_RTB_2015[0].Texto_2_Expand = "There are 25 hotels in Barcelona";
    dynamicContent.NH_Hoteles_RTB_2015[0].btn_gallery = "IMAGES";
    dynamicContent.NH_Hoteles_RTB_2015[0].Texto_seleccion = "OUR CHOICE";
    dynamicContent.NH_Hoteles_RTB_2015[0].cta_buscar = "find yours";
    dynamicContent.NH_Hoteles_RTB_2015[0].cta_buscar_url = {};
    dynamicContent.NH_Hoteles_RTB_2015[0].cta_buscar_url.Url = "http://www.nh-hotels.com/";
    dynamicContent.NH_Hoteles_RTB_2015[0].btn_volver = "back";
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_1_name = "HESPERIA FIRA SUITES";
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_1_imagen = {"thumbs_300x600.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099090/63009_20140930035443729_thumbs_300x600.jpg"},"thumbs_980x250.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099091/63009_20140930035448700_thumbs_980x250.jpg"}};
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_1_stars = 4;
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_1_rating = "4";
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_1_gallery = {"imagen_980x250_4.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34101620/63009_20140930035544771_imagen_980x250_4.jpg"},"imagen_980x250_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34100282/63009_20140930035534616_imagen_980x250_2.jpg"},"imagen_980x250_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34101710/63009_20140930035539416_imagen_980x250_3.jpg"},"imagen_980x250_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099095/63009_20140930035524533_imagen_980x250_1.jpg"},"imagen_300x600_4.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099094/63009_20140930035519236_imagen_300x600_4.jpg"},"imagen_300x600_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099093/63009_20140930035458820_imagen_300x600_2.jpg"},"imagen_300x600_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34100281/63009_20140930035509076_imagen_300x600_3.jpg"},"imagen_300x600_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099092/63009_20140930035454055_imagen_300x600_1.jpg"}};
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_1_cta_url = {};
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_1_cta_url.Url = "http://www.nh-hotels.com/";
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_2_name = "HESPERIA TOWER";
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_2_imagen = {"thumbs_980x250.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34100273/63009_20140930034903313_thumbs_980x250.jpg"},"thumbs_300x600.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099086/63009_20140930034854011_thumbs_300x600.jpg"}};
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_2_stars = 5;
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_2_rating = "3";
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_2_gallery = {"imagen_980x250_4.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34100480/63009_20140930035011987_imagen_980x250_4.jpg"},"imagen_980x250_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099495/63009_20140930035006385_imagen_980x250_3.jpg"},"imagen_980x250_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099494/63009_20140930034956315_imagen_980x250_2.jpg"},"imagen_980x250_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34100275/63009_20140930034946631_imagen_980x250_1.jpg"},"imagen_300x600_4.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099586/63009_20140930034935499_imagen_300x600_4.jpg"},"imagen_300x600_3.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099493/63009_20140930034923404_imagen_300x600_3.jpg"},"imagen_300x600_1.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34099585/63009_20140930034907254_imagen_300x600_1.jpg"},"imagen_300x600_2.jpg":{"Type":"file","Url":"https://s0.2mdn.net/ads/richmedia/studio/34101610/63009_20140930034917216_imagen_300x600_2.jpg"}};
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_2_cta_url = {};
    dynamicContent.NH_Hoteles_RTB_2015[0].hotel_2_cta_url.Url = "http://www.nh-hotels.com/";
    Enabler.setDevDynamicContent(dynamicContent);
    
   creative.dynamicData = dynamicContent.NH_Hoteles_RTB_2015[0];
  creative.domElements.txtFrame1.innerHTML = creative.dynamicData.Texto_2;
  creative.domElements.txtFrame2.innerHTML = creative.dynamicData.Texto_1;
  creative.domElements.textoFrame2Linea2.innerHTML = creative.dynamicData.Descuento + "<span>%</span>";
  creative.domElements.btnText.innerHTML = creative.dynamicData.cta
  creative.domElements.ctaUrl.innerHTML = creative.dynamicData.cta;
  creative.dynamicExitUrl = creative.dynamicData.URL_destino.Url;
  loopTotal = creative.dynamicData.Loop;
  descuento = creative.dynamicData.Descuento;

};


creative.closeClickHandler = function (event) {
  studioinnovation.youtube.requestYTAdClose('creative2yt_requestClose');
};

creative.exitClickHandler = function (event) {
  Enabler.counter('btn_frame_'+frame);
  Enabler.exitOverride("exit", creative.dynamicExitUrl);
  $(".frame1 .botonSuperior #btnText").stop(true, false);
  $(".frame1 .botonSuperior").stop(true, false);
  $(".texto").stop(true, false);
  $(".frame1 .faldon .logo").stop(true, false);
  $(".frame1 .faldon .boton").stop(true, false);
  $( ".frame1 .faldon .texto .textoFrame1" ).fadeIn( "slow");
  $( ".frame1 .faldon .texto .textoFrame2" ).fadeOut( "slow");
  $( ".frame1 .faldon .texto .textoFrame2Linea2" ).fadeOut( "slow");
  $(".frame1 .faldon .logo").css("width","89px");
  $(".frame1 .faldon .boton").css("margin-top","-40px");
  $(".frame1 .botonSuperior").css("margin-right","4px");
  $(".texto").css("width","254px");
  clearInterval(time);
  frame = 1;
};

creative.pageLoadHandler = function (event) {
  creative.initAd();
};

creative.initAd = function () {
  var external_javascript = document.createElement('script');
  external_javascript.setAttribute('type', 'text/javascript');
  external_javascript.setAttribute('src', Enabler.getUrl('assets/js/anim.js'));
  document.getElementsByTagName('head')[0].appendChild(external_javascript);
  var external_javascript = document.createElement('script');
  external_javascript.setAttribute('type', 'text/javascript');
  external_javascript.setAttribute('src', Enabler.getUrl('assets/js/polite.js'));
  document.getElementsByTagName('head')[0].appendChild(external_javascript);


  var external_css = document.createElement('link');
  external_css.setAttribute('rel', 'stylesheet');
  external_css.setAttribute('type', 'text/css');
  external_css.setAttribute('href', Enabler.getUrl('assets/css/style.css'));
  document.getElementsByTagName('head')[0].appendChild(external_css);

};

creative.showAd = function () {

  document.getElementById('content').className = "show";
  document.getElementById('loader').className = "hide";
  ini();
};


window.addEventListener('load', creative.init.bind(creative));
