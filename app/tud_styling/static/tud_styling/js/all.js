;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "accordion",
		defaults = {
			state: 'is-closed'
		},
		target = '.accordion';
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.$titles = this.$el.find('.accordion__title');
			this.$content = this.$el.find('.accordion__content');

			this.settings = $.extend( {}, defaults, options, this.$el.data() );
			this._name = pluginName;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				this.storeHeight();
				this.close();
				this.addEventlisteners()
			},
			addEventlisteners: function() {
				this.$titles.on('click', this.toggleSingle.bind(this));
			},
			storeHeight: function() {
				this.$content.each(function(i, elem) {
					$(this).data('origHeight', $(this).outerHeight())
				});
			},
			close: function(e) {
				var $title = (e) ? $(e.currentTarget) : this.$titles,
					$content = $title.next();

				$title.addClass(this.settings.state)
				$content.addClass(this.settings.state).css({
					height: 0
				})
			},
			open: function(e) {
				var $title = $(e.currentTarget),
					$content = $title.next();
				$title.removeClass(this.settings.state)
				$content
					.removeClass(this.settings.state)
					.css({height: $content.data('origHeight')})
			},
			toggleSingle: function(e) {
				e.preventDefault();
				if(/is-closed/.test(e.currentTarget.className)) {
					this.open(e);
				} else {
					this.close(e);
				}
				// $(e.currentTarget).siblings().addClass(this.settings.state);
				// $(e.currentTarget)
				// 	.toggleClass(this.settings.state)
				// 	next().toggleClass(this.settings.state);

				// //Toggles accordion__title and accordion__content with 'is-active' class
				// var content = $(e.currentTarget).next();
				// $(e.currentTarget)
				// 	.toggleClass(this.settings.state)
				// 	.next().css({height: content.data('origHeight')})
			},
			toggleAll: function(e) {
				this.close(e);
				this.open(e);
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};
	registerplugin(target, pluginName);

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "back_to_top",
		defaults = {
			minScroll: 200,
			// maxScroll: 'auto',
		},
		target = '.js-back_to_top';
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.settings = $.extend( {}, defaults, options, this.$el.data() );
			this._name = pluginName;
			this._defaults 	= defaults;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
		init: function () {
			this.calcHeight();
			this.addEventListeners();
		}
		, addEventListeners: function() {
			$(window).on('Katoen:ScrollEvent', this.toggleClasses.bind(this));
			this.$el.on('click', this.scrollTo.bind(this))
			$(window).on('Katoen:ResizeEvent', this.calcHeight.bind(this));

		}
		, calcHeight: function() {
			this.settings.maxScroll = $(document).height() - $('footer').outerHeight() + $('.nav-bottom').outerHeight();
		}
		, toggleClasses: function(e) {
			this.$el
				.toggleClass('is-fixed', e.latestKnownScroll.bottom >= this.settings.maxScroll)
				.toggleClass('up', e.direction == 'up' ||  e.latestKnownScroll.bottom >= this.settings.maxScroll)
				.toggleClass('show', e.latestKnownScroll.top > this.settings.minScroll)
		}
		, scrollTo: function(e) {
			e.preventDefault();
			if($(e.currentTarget).hasClass('up')) {
				$("html, body").animate({ scrollTop: 0 });
			} else {
				$("html, body").animate({ scrollTop: $('footer').position().top });
			}
		}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};
	
	$(window).on('load', function() {
		$(target)[pluginName]()
	});

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "breadcrumb",
		defaults = {},
		target = '.breadcrumb';
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.settings = $.extend( {}, options, this.$el.data() );
			this._name = pluginName;
			this._defaults 	= defaults;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				this.$el.scrollLeft(9999);
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};
	
	$(window).on('load', function() {

		setTimeout(function() { $(target)[pluginName]() }, 400);
	});

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "carousel",
		target = '.carousel__slides'

	function Plugin ( element, options ) {
			this.$el = $(element);
			this.$dropdown = $('.nav-carousel')

			this.$children = this.$el.children();
			this.settings = $.extend( {}, options, this.$el.data() );
			this._name = pluginName;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				this.slidesLoaded = 0;
				this.totalSlides = this.$children.length;

				this.addEventListeners();
				this.buildDropdown();
			},
			addEventListeners:function() {
				this.$el.on("Katoen:ResponsiveImageLoaded", this.buildSlider.bind(this));
				this.$dropdown.on('click', '.label', this.openDropdown.bind(this));
				$(window).on("Katoen:ResizeEvent", this.buildDropdown.bind(this));
			},
			buildSlider: function(e) {
				this.slidesLoaded++;

				if (this.slidesLoaded >= this.totalSlides) {
					this.slidesLoaded = 0;
					this.$el.off("Katoen:ResponsiveImageLoaded");

					// this.$el.find('.poster__content').css({minHeight: this.$dropdown.outerHeight() + 200 })
					//Check to see if dropdown is higher than slider, if so; adjust

					this.$el.slick({
						// options
						adaptiveHeight: true,
						centerMode: true,
						centerPadding: 0,
						appendArrows: this.$el.parent().find('.carousel__arrowcontainer'),
						prevArrow: '<button class="btn--icon carousel__prev"><i class="onhover-arrow_left">',
						nextArrow: '<button class="btn--icon carousel__next"><i class="onhover-arrow_right">'
					});

					var dropdownHeight = this.$dropdown.outerHeight(),
						carouselHeight = this.$el.outerHeight();
						
					if (carouselHeight <= dropdownHeight + 200) {
						this.$el.find('.poster__content').css({minHeight: dropdownHeight + 200})
					}
				}
			},
			isSmall: function() {
				return ['xs', 'sm'].indexOf(document.currMedia) !== -1;
			},
			buildDropdown: function(e) {
				//Adds arrow if wrong breakpoint
				this.$dropdown.find('.label').toggleClass('i-arrow_select-after', this.isSmall());
			},
			openDropdown: function(e) {
				if(this.isSmall() && e.currentTarget == e.target) {
					$(e.currentTarget).parent().toggleClass('is-active');
				}
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};

	registerplugin(target, pluginName)

})( jQuery, window, document );


//  $('.slider-for').slick({
//   slidesToShow: 1,
//   slidesToScroll: 1,
//   arrows: false,
//   fade: true,
//   asNavFor: '.slider-nav'
// });
// $('.slider-nav').slick({
//   slidesToShow: 3,
//   slidesToScroll: 1,
//   asNavFor: '.slider-for',
//   dots: true,
//   centerMode: true,
//   focusOnSelect: true
// });
//        
;
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "gallery",
		target = '.gallery'

	function Plugin ( element, options ) {
			this.$el = $(element);
			this.$children = this.$el.children();
			this.settings = $.extend( {}, options, this.$el.data() );
			this._name = pluginName;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				//No slider needed, less than 5 images
				if(this.$children.length < 5) {
					this.$children
						.addClass('sm-'+(12/this.$children.length))
						.each(this.checkFit.bind(this));
				} else {
					//Oops! More than 5 images means the slider is initialized
					this.$el.wrap('<div class="gallery-slider">');

					//Copy current dom to above current element for thumbnail navigation
					this.$paging = this.$el.clone().addClass('slick-paging');
					this.$paging.find('figcaption').remove();
					
					this.$el.after(this.$paging);


					this.$el.slick({
						// options
						centerMode: true,
						centerPadding: 0,
						asNavFor: this.$paging[0],
						arrows: false,
					});

					this.$paging.slick({
						centerMode: true,
						slidesToShow: 3,
						slidesToScroll: 1,
						focusOnSelect: true,
						asNavFor: this.$el[0],
						prevArrow: '<button class="slick-prev">',
						nextArrow: '<button class="slick-next">'
					});
				}
			},
			checkFit: function(i, e) {
				if($('img', e).width() != $('figcaption', e).width()) {
					// img is not the same length as figcaption, must be next to each other
					$('figcaption', e).css({paddingLeft: '1rem', paddingTop: 0 })
				}
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};

	registerplugin(target, pluginName)

})( jQuery, window, document );


//  $('.slider-for').slick({
//   slidesToShow: 1,
//   slidesToScroll: 1,
//   arrows: false,
//   fade: true,
//   asNavFor: '.slider-nav'
// });
// $('.slider-nav').slick({
//   slidesToShow: 3,
//   slidesToScroll: 1,
//   asNavFor: '.slider-for',
//   dots: true,
//   centerMode: true,
//   focusOnSelect: true
// });
//        
;
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "modal",
		target = '.js-modal',
		defaults = {
			origsrc: 'hi',
			state: 'is-active',
			markup: 
				'<div class="modal">\
					<button class="menu menu--close button-reset js-toggle" data-target="this.parent">\
						<i class="i-close"></i>\
					</button>\
					<div class="modal__content">\
					</div>\
				</div>\
				'

		};
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.settings = $.extend( {}, defaults, options, this.$el.data() );
			
			this.$target = $(this.settings.target || this.$el);
			//Test selector for 'this', so we can traverse the DOM in the DOM
			if(/this/.test(this.settings.target)) {
				var sub = this.settings.target.substring(5);
				this.$target = this.$el[sub]();
			}
			//Hide target
			this.$target.hide();

			this._name = pluginName;

			//Check to see if modal has already run, and doesn't need to be anymore
			this.init();
	}
	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function (e) {
				//Creates single instance of the modal
				if(!this.initialized()) {
					//Adds markup to the dom
					$('body').prepend(this.settings.markup);
				}
				this.$modal = $('.modal');

				this.addEventlisteners();
			},
			initialized: function(e) {
				return $('.modal')[0] != undefined
			},
			addEventlisteners: function() {
				this.$el.on('click', this.open.bind(this));
				
				//On modal click if it doesn't already have the event, close the modal
				if(!$._data( this.$modal[0], 'events' )) {
					this.$modal.on('click', this.toggle.bind(this));
				}
			},
			toggle: function(e) {
				var re = new RegExp(this.settings.state)
				if(e.target != e.currentTarget) {
					if(!re.test(this.$modal[0].className)) {
						this.open(e);
					}
				} else {
					this.close(e);
				}
			},
			open: function(e) {
				//Moves html to modal content
			// [R R] BEGIN
			// [R R] not a cookie-law friendly solution. It just shows html that was first hidden with display: none. We need to change this code for things like videos, iframes or scripttags when cookie-law is in effect again.
			//	this.$modal.find('.modal__content').html(this.$target.show())
				console.log(this.$modal);
				var contentEl = this.$modal.find('.modal__content');
				contentEl.html(this.$target.show());

				var divEl = this.$target.find('.source');
				if (divEl) {
					var iframeEl = this.$target.find('iframe');
					var src = divEl.attr('data-src');
					if (src) {
						// [R R] check for youtube or vimeo in the src
						var str=src.match(/\/\/(www[0-9]?\.)?(.[^/:]+)(\.com|\.nl)/)[2];
						
						// [R R] add extra parameters to the url; start playing the video
						switch(str) {
							case 'youtube':
								src += '?&autoplay=1&rel=0'
								break;
								
							case 'player.vimeo':
								src += '?&autoplay=1'
								break;
						}
						iframeEl.attr('src', src);
					}
				}
				// [R R] END
				
				this.$modal.addClass(this.settings.state);
				$(window).on('keyup', this.close.bind(this));
			},
			close: function(e) {
				// [R R] BEGIN
				// [R R] replace the generated url with about:blank; stop the video from playing while hidden
				this.$modal.find('iframe').attr('src', 'about:blank');
				// [R R] END
				
				//If escape, close modal
				if (e.keyCode && e.keyCode != 27) { return }
				this.$modal.removeClass(this.settings.state);
				$(window).off('keyup', this.close);
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
		return this.each(function() {
			if ( !$.data( this, "plugin_" + pluginName ) ) {
				$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
			}
		});
	};

	registerplugin(target, pluginName);

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "nav-fit",
		target = ".nav-bottom, .nav-top",
		defaults = {
			controlHeight: 60, //Height of nav bar
			autoHeight: false,
			moreTemplate: '<button class="button-reset btn--icon i-more js-toggle" data-target=".nav-overlay"></button>'
		};
		
	function Plugin ( element, options ) {
			this.$el 		= $(element);
			this.settings 	= $.extend( {}, defaults, options, this.$el.data() );

			this._name 		= pluginName;
			this._defaults 	= defaults;
			this._itemsShown= 0;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				if(this.settings.autoHeight == true) {
					//Finds a navigation item to set the height.
					this.settings.controlHeight = this.$el.find('a').outerHeight();
				}
				//Find items with data-priorty and sort them, and hide them
				this.$items = this.$el.find('[data-priority]');
				//Sort by priority [9-0]
				this.$items.sort(function(a,b) {
					a = $(a), b = $(b)
					return a.attr('data-priority') < b.attr('data-priority')
				});

				this.addEventlisteners();
				this.addMoreButton();
				this.reFit();
			},
			addMoreButton: function() {
				this.$moreBtn = $(this.settings.moreTemplate).insertAfter( this.$items.parent() );
			},
			addEventlisteners: function() {
				$(window).on('Katoen:ResizeEvent', this.reFit.bind(this));
				$(window).on('load', this.reFit.bind(this));
			},
			reFit: function(e) {
				this.$items.show();
				this.$moreBtn.hide();
				//Loop through all navigation items, hide them one by one
				//and hide them only if it doesn't fit anymore
				for (var i = this.$items.length - 1; i >= 0; i--) {
					if(!this.doesFit()) {
						this.$items.eq(i).hide();
						this.$moreBtn.show();
					} else {
						break;
					}
				};
			},
			doesFit: function() {
				return this.$el.outerHeight() <= this.settings.controlHeight
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};
	registerplugin(target, pluginName);

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "nav-overlay",
		target = '.nav-overlay',
		defaults = {
			state: 'is-active'
		};
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.settings = $.extend( {}, defaults, options, this.$el.data() );
			this._name = pluginName;
			
			this.init();
	}
	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function (e) {
				this.addEventlisteners();
			},
			addEventlisteners: function() {
				this.$el.on('click', '.nav-overlay__mainitem', this.toggle.bind(this));
			},
			toggle: function(e) {
				$(e.currentTarget).parent().siblings().removeClass(this.settings.state);
				$(e.currentTarget).parent().toggleClass(this.settings.state);
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
		return this.each(function() {
			if ( !$.data( this, "plugin_" + pluginName ) ) {
				$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
			}
		});
	};

	registerplugin(target, pluginName);

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "nav-tab",
		target = '.nav-tab';
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.settings = $.extend( {}, options, this.$el.data() );
			this._name = pluginName;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				this.addEventlisteners()
			},
			addEventlisteners: function() {
				this.$el.on('click', 'a', this.toggleTab.bind(this));
			},
			toggleTab: function(e) {
				e.preventDefault();
				var $currTab = $(e.currentTarget),
					$currTarget = $currTab.attr('target') ? $($currTab.attr('target')) : this.$el.siblings().eq($currTab.parent().index());
				//Remove all active states from tabs
				this.$el.parent().find('.is-active').removeClass('is-active')
				
				//Add active state to relevant tabs, and content
				$currTab.addClass('is-active');
				$currTarget.addClass('is-active');
				// this.$el.siblings($currTab.attr('target')).addClass('is-active');
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};
	registerplugin(target, pluginName);

})( jQuery, window, document );
/*! Picturefill - v3.0.0-alpha1 - 2015-06-24
* http://scottjehl.github.io/picturefill
* Copyright (c) 2015 https://github.com/scottjehl/picturefill/blob/master/Authors.txt; Licensed MIT */

(function(window) {
	/*jshint eqnull:true */
	var ua = navigator.userAgent;

	if ( window.HTMLPictureElement && ((/ecko/).test(ua) && ua.match(/rv\:(\d+)/) && RegExp.$1 < 41) ) {
		addEventListener("resize", (function() {
			var timer;

			var dummySrc = document.createElement("source");

			var fixRespimg = function(img) {
				var source, sizes;
				var picture = img.parentNode;

				if (picture.nodeName.toUpperCase() === "PICTURE") {
					source = dummySrc.cloneNode();

					picture.insertBefore(source, picture.firstElementChild);
					setTimeout(function() {
						picture.removeChild(source);
					});
				} else if (!img._pfLastSize || img.offsetWidth > img._pfLastSize) {
					img._pfLastSize = img.offsetWidth;
					sizes = img.sizes;
					img.sizes += ",100vw";
					setTimeout(function() {
						img.sizes = sizes;
					});
				}
			};

			var findPictureImgs = function() {
				var i;
				var imgs = document.querySelectorAll("picture > img, img[srcset][sizes]");
				for (i = 0; i < imgs.length; i++) {
					fixRespimg(imgs[i]);
				}
			};
			var onResize = function() {
				clearTimeout(timer);
				timer = setTimeout(findPictureImgs, 99);
			};
			var mq = window.matchMedia && matchMedia("(orientation: landscape)");
			var init = function() {
				onResize();

				if (mq && mq.addListener) {
					mq.addListener(onResize);
				}
			};

			dummySrc.srcset = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==";

			if (/^[c|i]|d$/.test(document.readyState || "")) {
				init();
			} else {
				document.addEventListener("DOMContentLoaded", init);
			}

			return onResize;
		})());
	}
})(window);

/*! Picturefill - Responsive Images that work today.
 *  Author: Scott Jehl, Filament Group, 2012 ( new proposal implemented by Shawn Jansepar )
 *  License: MIT
 *  Spec: http://picture.responsiveimages.org/
 */
(function( window, document, undefined ) {
	/* global parseSizes */
	// Enable strict mode
	"use strict";

	// HTML shim|v it for old IE (IE9 will still need the HTML video tag workaround)
	document.createElement( "picture" );

	var warn, eminpx, alwaysCheckWDescriptor, evalId;
	// local object for method references and testing exposure
	var pf = {};
	var noop = function() {};
	var image = document.createElement( "img" );
	var getImgAttr = image.getAttribute;
	var setImgAttr = image.setAttribute;
	var removeImgAttr = image.removeAttribute;
	var docElem = document.documentElement;
	var types = {};
	var cfg = {
		//resource selection:
		algorithm: ""
	};
	var srcAttr = "data-pfsrc";
	var srcsetAttr = srcAttr + "set";
	// ua sniffing is done for undetectable img loading features,
	// to do some non crucial perf optimizations
	var ua = navigator.userAgent;
	var supportAbort = (/rident/).test(ua) || ((/ecko/).test(ua) && ua.match(/rv\:(\d+)/) && RegExp.$1 > 35 );
	var curSrcProp = "currentSrc";
	var regWDesc = /\s+\+?\d+(e\d+)?w/;
	var regSize = /(\([^)]+\))?\s*(.+)/;
	var setOptions = window.picturefillCFG;
	/**
	 * Shortcut property for https://w3c.github.io/webappsec/specs/mixedcontent/#restricts-mixed-content ( for easy overriding in tests )
	 */
	// baseStyle also used by getEmValue (i.e.: width: 1em is important)
	var baseStyle = "position:absolute;left:0;visibility:hidden;display:block;padding:0;border:none;font-size:1em;width:1em;overflow:hidden;clip:rect(0px, 0px, 0px, 0px)";
	var fsCss = "font-size:100%!important;";
	var isVwDirty = true;

	var cssCache = {};
	var sizeLengthCache = {};
	var DPR = window.devicePixelRatio;
	var units = {
		px: 1,
		"in": 96
	};
	var anchor = document.createElement( "a" );
	/**
	 * alreadyRun flag used for setOptions. is it true setOptions will reevaluate
	 * @type {boolean}
	 */
	var alreadyRun = false;

	// Reusable, non-"g" Regexes

	// (Don't use \s, to avoid matching non-breaking space.)
	var regexLeadingSpaces = /^[ \t\n\r\u000c]+/,
	    regexLeadingCommasOrSpaces = /^[, \t\n\r\u000c]+/,
	    regexLeadingNotSpaces = /^[^ \t\n\r\u000c]+/,
	    regexTrailingCommas = /[,]+$/,
	    regexNonNegativeInteger = /^\d+$/,

	    // ( Positive or negative or unsigned integers or decimals, without or without exponents.
	    // Must include at least one digit.
	    // According to spec tests any decimal point must be followed by a digit.
	    // No leading plus sign is allowed.)
	    // https://html.spec.whatwg.org/multipage/infrastructure.html#valid-floating-point-number
	    regexFloatingPoint = /^-?(?:[0-9]+|[0-9]*\.[0-9]+)(?:[eE][+-]?[0-9]+)?$/;

	var on = function(obj, evt, fn, capture) {
		if ( obj.addEventListener ) {
			obj.addEventListener(evt, fn, capture || false);
		} else if ( obj.attachEvent ) {
			obj.attachEvent( "on" + evt, fn);
		}
	};

	/**
	 * simple memoize function:
	 */

	var memoize = function(fn) {
		var cache = {};
		return function(input) {
			if ( !(input in cache) ) {
				cache[ input ] = fn(input);
			}
			return cache[ input ];
		};
	};

	// UTILITY FUNCTIONS

	// Manual is faster than RegEx
	// http://jsperf.com/whitespace-character/5
	function isSpace(c) {
		return (c === "\u0020" || // space
		        c === "\u0009" || // horizontal tab
		        c === "\u000A" || // new line
		        c === "\u000C" || // form feed
		        c === "\u000D");  // carriage return
	}

	/**
	 * gets a mediaquery and returns a boolean or gets a css length and returns a number
	 * @param css mediaqueries or css length
	 * @returns {boolean|number}
	 *
	 * based on: https://gist.github.com/jonathantneal/db4f77009b155f083738
	 */
	var evalCSS = (function() {

		var regLength = /^([\d\.]+)(em|vw|px)$/;
		var replace = function() {
			var args = arguments, index = 0, string = args[0];
			while (++index in args) {
				string = string.replace(args[index], args[++index]);
			}
			return string;
		};

		var buidlStr = memoize(function(css) {

			return "return " + replace((css || "").toLowerCase(),
				// interpret `and`
				/\band\b/g, "&&",

				// interpret `,`
				/,/g, "||",

				// interpret `min-` as >=
				/min-([a-z-\s]+):/g, "e.$1>=",

				// interpret `max-` as <=
				/max-([a-z-\s]+):/g, "e.$1<=",

				//calc value
				/calc([^)]+)/g, "($1)",

				// interpret css values
				/(\d+[\.]*[\d]*)([a-z]+)/g, "($1 * e.$2)",
				//make eval less evil
				/^(?!(e.[a-z]|[0-9\.&=|><\+\-\*\(\)\/])).*/ig, ""
			) + ";";
		});

		return function(css, length) {
			var parsedLength;
			if (!(css in cssCache)) {
				cssCache[css] = false;
				if (length && (parsedLength = css.match( regLength ))) {
					cssCache[css] = parsedLength[ 1 ] * units[parsedLength[ 2 ]];
				} else {
					/*jshint evil:true */
					try{
						cssCache[css] = new Function("e", buidlStr(css))(units);
					} catch(e) {}
					/*jshint evil:false */
				}
			}
			return cssCache[css];
		};
	})();

	var setResolution = function( candidate, sizesattr ) {
		if ( candidate.w ) { // h = means height: || descriptor.type === 'h' do not handle yet...
			candidate.cWidth = pf.calcListLength( sizesattr || "100vw" );
			candidate.res = candidate.w / candidate.cWidth ;
		} else {
			candidate.res = candidate.d;
		}
		return candidate;
	};

	/**
	 *
	 * @param opt
	 */
	var picturefill = function( opt ) {
		var elements, i, plen;

		var options = opt || {};

		if ( options.elements && options.elements.nodeType === 1 ) {
			if ( options.elements.nodeName.toUpperCase() === "IMG" ) {
				options.elements =  [ options.elements ];
			} else {
				options.context = options.elements;
				options.elements =  null;
			}
		}

		elements = options.elements || pf.qsa( (options.context || document), ( options.reevaluate || options.reselect ) ? pf.sel : pf.selShort );

		if ( (plen = elements.length) ) {

			pf.setupRun( options );
			alreadyRun = true;

			// Loop through all elements
			for ( i = 0; i < plen; i++ ) {
				pf.fillImg(elements[ i ], options);
			}

			pf.teardownRun( options );
		}
	};

	/**
	 * outputs a warning for the developer
	 * @param {message}
	 * @type {Function}
	 */
	warn = ( window.console && console.warn ) ?
		function( message ) {
			console.warn( message );
		} :
		noop
	;

	if ( !(curSrcProp in image) ) {
		curSrcProp = "src";
	}

	// Add support for standard mime types.
	types[ "image/jpeg" ] = true;
	types[ "image/gif" ] = true;
	types[ "image/png" ] = true;

	function detectTypeSupport( type, typeUri ) {
		// based on Modernizr's lossless img-webp test
		// note: asynchronous
		var image = new window.Image();
		image.onerror = function() {
			types[ type ] = false;
			picturefill();
		};
		image.onload = function() {
			types[ type ] = image.width === 1;
			picturefill();
		};
		image.src = typeUri;
		return "pending";
	}

	// test svg support
	types[ "image/svg+xml" ] = document.implementation.hasFeature( "http://wwwindow.w3.org/TR/SVG11/feature#Image", "1.1" );

	/**
	 * updates the internal vW property with the current viewport width in px
	 */
	function updateMetrics() {

		isVwDirty = false;
		DPR = window.devicePixelRatio;
		cssCache = {};
		sizeLengthCache = {};

		pf.DPR = DPR || 1;

		units.width = Math.max(window.innerWidth || 0, docElem.clientWidth);
		units.height = Math.max(window.innerHeight || 0, docElem.clientHeight);

		units.vw = units.width / 100;
		units.vh = units.height / 100;

		evalId = [ units.height, units.width, DPR ].join("-");

		units.em = pf.getEmValue();
		units.rem = units.em;
	}

	function chooseLowRes( lowerValue, higherValue, dprValue, isCached ) {
		var bonusFactor, tooMuch, bonus, meanDensity;

		//experimental
		if (cfg.algorithm === "saveData" ){
			if ( lowerValue > 2.7 ) {
				meanDensity = dprValue + 1;
			} else {
				tooMuch = higherValue - dprValue;
				bonusFactor = Math.pow(lowerValue - 0.6, 1.5);

				bonus = tooMuch * bonusFactor;

				if (isCached) {
					bonus += 0.1 * bonusFactor;
				}

				meanDensity = lowerValue + bonus;
			}
		} else {
			meanDensity = (dprValue > 1) ?
				Math.sqrt(lowerValue * higherValue) :
				lowerValue;
		}

		return meanDensity > dprValue;
	}

	function applyBestCandidate( img ) {
		var srcSetCandidates;
		var matchingSet = pf.getSet( img );
		var evaluated = false;
		if ( matchingSet !== "pending" ) {
			evaluated = evalId;
			if ( matchingSet ) {
				srcSetCandidates = pf.setRes( matchingSet );
				pf.applySetCandidate( srcSetCandidates, img );
			}
		}
		img[ pf.ns ].evaled = evaluated;
	}

	function ascendingSort( a, b ) {
		return a.res - b.res;
	}

	function setSrcToCur( img, src, set ) {
		var candidate;
		if ( !set && src ) {
			set = img[ pf.ns ].sets;
			set = set && set[set.length - 1];
		}

		candidate = getCandidateForSrc(src, set);

		if ( candidate ) {
			src = pf.makeUrl(src);
			img[ pf.ns ].curSrc = src;
			img[ pf.ns ].curCan = candidate;

			if ( !candidate.res ) {
				setResolution( candidate, candidate.set.sizes );
			}
		}
		return candidate;
	}

	function getCandidateForSrc( src, set ) {
		var i, candidate, candidates;
		if ( src && set ) {
			candidates = pf.parseSet( set );
			src = pf.makeUrl(src);
			for ( i = 0; i < candidates.length; i++ ) {
				if ( src === pf.makeUrl(candidates[ i ].url) ) {
					candidate = candidates[ i ];
					break;
				}
			}
		}
		return candidate;
	}

	function getAllSourceElements( picture, candidates ) {
		var i, len, source, srcset;

		// SPEC mismatch intended for size and perf:
		// actually only source elements preceding the img should be used
		// also note: don't use qsa here, because IE8 sometimes doesn't like source as the key part in a selector
		var sources = picture.getElementsByTagName( "source" );

		for ( i = 0, len = sources.length; i < len; i++ ) {
			source = sources[ i ];
			source[ pf.ns ] = true;
			srcset = source.getAttribute( "srcset" );

			// if source does not have a srcset attribute, skip
			if ( srcset ) {
				candidates.push( {
					srcset: srcset,
					media: source.getAttribute( "media" ),
					type: source.getAttribute( "type" ),
					sizes: source.getAttribute( "sizes" )
				} );
			}
		}
	}

	/**
	 * Srcset Parser
	 * By Alex Bell |  MIT License
	 *
	 * @returns Array [{url: _, d: _, w: _, h:_, set:_(????)}, ...]
	 *
	 * Based super duper closely on the reference algorithm at:
	 * https://html.spec.whatwg.org/multipage/embedded-content.html#parse-a-srcset-attribute
	 */

	// 1. Let input be the value passed to this algorithm.
	// (TO-DO : Explain what "set" argument is here. Maybe choose a more
	// descriptive & more searchable name.  Since passing the "set" in really has
	// nothing to do with parsing proper, I would prefer this assignment eventually
	// go in an external fn.)
	function parseSrcset(input, set) {

		function collectCharacters(regEx) {
			var chars,
			    match = regEx.exec(input.substring(pos));
			if (match) {
				chars = match[ 0 ];
				pos += chars.length;
				return chars;
			}
		}

		var inputLength = input.length,
		    url,
		    descriptors,
		    currentDescriptor,
		    state,
		    c,

		    // 2. Let position be a pointer into input, initially pointing at the start
		    //    of the string.
		    pos = 0,

		    // 3. Let candidates be an initially empty source set.
		    candidates = [];

		/**
		* Adds descriptor properties to a candidate, pushes to the candidates array
		* @return undefined
		*/
		// (Declared outside of the while loop so that it's only created once.
		// (This fn is defined before it is used, in order to pass JSHINT.
		// Unfortunately this breaks the sequencing of the spec comments. :/ )
		function parseDescriptors() {

			// 9. Descriptor parser: Let error be no.
			var pError = false,

			// 10. Let width be absent.
			// 11. Let density be absent.
			// 12. Let future-compat-h be absent. (We're implementing it now as h)
			    w, d, h, i,
			    candidate = {},
			    desc, lastChar, value, intVal, floatVal;

			// 13. For each descriptor in descriptors, run the appropriate set of steps
			// from the following list:
			for (i = 0 ; i < descriptors.length; i++) {
				desc = descriptors[ i ];

				lastChar = desc[ desc.length - 1 ];
				value = desc.substring(0, desc.length - 1);
				intVal = parseInt(value, 10);
				floatVal = parseFloat(value);

				// If the descriptor consists of a valid non-negative integer followed by
				// a U+0077 LATIN SMALL LETTER W character
				if (regexNonNegativeInteger.test(value) && (lastChar === "w")) {

					// If width and density are not both absent, then let error be yes.
					if (w || d) {pError = true;}

					// Apply the rules for parsing non-negative integers to the descriptor.
					// If the result is zero, let error be yes.
					// Otherwise, let width be the result.
					if (intVal === 0) {pError = true;} else {w = intVal;}

				// If the descriptor consists of a valid floating-point number followed by
				// a U+0078 LATIN SMALL LETTER X character
				} else if (regexFloatingPoint.test(value) && (lastChar === "x")) {

					// If width, density and future-compat-h are not all absent, then let error
					// be yes.
					if (w || d || h) {pError = true;}

					// Apply the rules for parsing floating-point number values to the descriptor.
					// If the result is less than zero, let error be yes. Otherwise, let density
					// be the result.
					if (floatVal < 0) {pError = true;} else {d = floatVal;}

				// If the descriptor consists of a valid non-negative integer followed by
				// a U+0068 LATIN SMALL LETTER H character
				} else if (regexNonNegativeInteger.test(value) && (lastChar === "h")) {

					// If height and density are not both absent, then let error be yes.
					if (h || d) {pError = true;}

					// Apply the rules for parsing non-negative integers to the descriptor.
					// If the result is zero, let error be yes. Otherwise, let future-compat-h
					// be the result.
					if (intVal === 0) {pError = true;} else {h = intVal;}

				// Anything else, Let error be yes.
				} else {pError = true;}
			} // (close step 13 for loop)

			// 15. If error is still no, then append a new image source to candidates whose
			// URL is url, associated with a width width if not absent and a pixel
			// density density if not absent. Otherwise, there is a parse error.
			if (!pError) {
				candidate.url = url;

				if (w) { candidate.w = w;}
				if (d) { candidate.d = d;}
				if (h) { candidate.h = h;}
				if (!h && !d && !w) {candidate.d = 1;}
				if (candidate.d === 1) {set.has1x = true;}
				candidate.set = set;

				candidates.push(candidate);
			}
		} // (close parseDescriptors fn)

		/**
		* Tokenizes descriptor properties prior to parsing
		* Returns undefined.
		* (Again, this fn is defined before it is used, in order to pass JSHINT.
		* Unfortunately this breaks the logical sequencing of the spec comments. :/ )
		*/
		function tokenize() {

			// 8.1. Descriptor tokeniser: Skip whitespace
			collectCharacters(regexLeadingSpaces);

			// 8.2. Let current descriptor be the empty string.
			currentDescriptor = "";

			// 8.3. Let state be in descriptor.
			state = "in descriptor";

			while (true) {

				// 8.4. Let c be the character at position.
				c = input.charAt(pos);

				//  Do the following depending on the value of state.
				//  For the purpose of this step, "EOF" is a special character representing
				//  that position is past the end of input.

				// In descriptor
				if (state === "in descriptor") {
					// Do the following, depending on the value of c:

				  // Space character
				  // If current descriptor is not empty, append current descriptor to
				  // descriptors and let current descriptor be the empty string.
				  // Set state to after descriptor.
					if (isSpace(c)) {
						if (currentDescriptor) {
							descriptors.push(currentDescriptor);
							currentDescriptor = "";
							state = "after descriptor";
						}

					// U+002C COMMA (,)
					// Advance position to the next character in input. If current descriptor
					// is not empty, append current descriptor to descriptors. Jump to the step
					// labeled descriptor parser.
					} else if (c === ",") {
						pos += 1;
						if (currentDescriptor) {
							descriptors.push(currentDescriptor);
						}
						parseDescriptors();
						return;

					// U+0028 LEFT PARENTHESIS (()
					// Append c to current descriptor. Set state to in parens.
					} else if (c === "\u0028") {
						currentDescriptor = currentDescriptor + c;
						state = "in parens";

					// EOF
					// If current descriptor is not empty, append current descriptor to
					// descriptors. Jump to the step labeled descriptor parser.
					} else if (c === "") {
						if (currentDescriptor) {
							descriptors.push(currentDescriptor);
						}
						parseDescriptors();
						return;

					// Anything else
					// Append c to current descriptor.
					} else {
						currentDescriptor = currentDescriptor + c;
					}
				// (end "in descriptor"

				// In parens
				} else if (state === "in parens") {

					// U+0029 RIGHT PARENTHESIS ())
					// Append c to current descriptor. Set state to in descriptor.
					if (c === ")") {
						currentDescriptor = currentDescriptor + c;
						state = "in descriptor";

					// EOF
					// Append current descriptor to descriptors. Jump to the step labeled
					// descriptor parser.
					} else if (c === "") {
						descriptors.push(currentDescriptor);
						parseDescriptors();
						return;

					// Anything else
					// Append c to current descriptor.
					} else {
						currentDescriptor = currentDescriptor + c;
					}

				// After descriptor
				} else if (state === "after descriptor") {

					// Do the following, depending on the value of c:
					// Space character: Stay in this state.
					if (isSpace(c)) {

					// EOF: Jump to the step labeled descriptor parser.
					} else if (c === "") {
						parseDescriptors();
						return;

					// Anything else
					// Set state to in descriptor. Set position to the previous character in input.
					} else {
						state = "in descriptor";
						pos -= 1;

					}
				}

				// Advance position to the next character in input.
				pos += 1;

			// Repeat this step.
			} // (close while true loop)
		}

		// 4. Splitting loop: Collect a sequence of characters that are space
		//    characters or U+002C COMMA characters. If any U+002C COMMA characters
		//    were collected, that is a parse error.
		while (true) {
			collectCharacters(regexLeadingCommasOrSpaces);

			// 5. If position is past the end of input, return candidates and abort these steps.
			if (pos >= inputLength) {
				return candidates; // (we're done, this is the sole return path)
			}

			// 6. Collect a sequence of characters that are not space characters,
			//    and let that be url.
			url = collectCharacters(regexLeadingNotSpaces);

			// 7. Let descriptors be a new empty list.
			descriptors = [];

			// 8. If url ends with a U+002C COMMA character (,), follow these substeps:
			//		(1). Remove all trailing U+002C COMMA characters from url. If this removed
			//         more than one character, that is a parse error.
			if (url.slice(-1) === ",") {
				url = url.replace(regexTrailingCommas, "");
				// (Jump ahead to step 9 to skip tokenization and just push the candidate).
				parseDescriptors();

			//	Otherwise, follow these substeps:
			} else {
				tokenize();
			} // (close else of step 8)

		// 16. Return to the step labeled splitting loop.
		} // (Close of big while loop.)
	}

	/* jshint ignore:start */
	// jscs:disable

	/*
	 * Sizes Parser
	 *
	 * By Alex Bell |  MIT License
	 *
	 * Non-strict but accurate and lightweight JS Parser for the string value <img sizes="here">
	 *
	 * Reference algorithm at:
	 * https://html.spec.whatwg.org/multipage/embedded-content.html#parse-a-sizes-attribute
	 *
	 * Most comments are copied in directly from the spec
	 * (except for comments in parens).
	 *
	 * Grammar is:
	 * <source-size-list> = <source-size># [ , <source-size-value> ]? | <source-size-value>
	 * <source-size> = <media-condition> <source-size-value>
	 * <source-size-value> = <length>
	 * http://www.w3.org/html/wg/drafts/html/master/embedded-content.html#attr-img-sizes
	 *
	 * E.g. "(max-width: 30em) 100vw, (max-width: 50em) 70vw, 100vw"
	 * or "(min-width: 30em), calc(30vw - 15px)" or just "30vw"
	 *
	 * Returns the first valid <css-length> with a media condition that evaluates to true,
	 * or "100vw" if all valid media conditions evaluate to false.
	 *
	 */

	function parseSizes(strValue) {

		// (Percentage CSS lengths are not allowed in this case, to avoid confusion:
		// https://html.spec.whatwg.org/multipage/embedded-content.html#valid-source-size-list
		// CSS allows a single optional plus or minus sign:
		// http://www.w3.org/TR/CSS2/syndata.html#numbers
		// CSS is ASCII case-insensitive:
		// http://www.w3.org/TR/CSS2/syndata.html#characters )
		// Spec allows exponential notation for <number> type:
		// http://dev.w3.org/csswg/css-values/#numbers
		var regexCssLengthWithUnits = /^(?:[+-]?[0-9]+|[0-9]*\.[0-9]+)(?:[eE][+-]?[0-9]+)?(?:ch|cm|em|ex|in|mm|pc|pt|px|rem|vh|vmin|vmax|vw)$/i;

		// (This is a quick and lenient test. Because of optional unlimited-depth internal
		// grouping parens and strict spacing rules, this could get very complicated.)
		var regexCssCalc = /^calc\((?:[0-9a-z \.\+\-\*\/\(\)]+)\)$/i;

		var i;
		var unparsedSizesList;
		var unparsedSizesListLength;
		var unparsedSize;
		var lastComponentValue;
		var size;

		// UTILITY FUNCTIONS

		//  (Toy CSS parser. The goals here are:
		//  1) expansive test coverage without the weight of a full CSS parser.
		//  2) Avoiding regex wherever convenient.
		//  Quick tests: http://jsfiddle.net/gtntL4gr/3/
		//  Returns an array of arrays.)
		function parseComponentValues(str) {
			var chrctr;
			var component = "";
			var componentArray = [];
			var listArray = [];
			var parenDepth = 0;
			var pos = 0;
			var inComment = false;

			function pushComponent() {
				if (component) {
					componentArray.push(component);
					component = "";
				}
			}

			function pushComponentArray() {
				if (componentArray[0]) {
					listArray.push(componentArray);
					componentArray = [];
				}
			}

			// (Loop forwards from the beginning of the string.)
			while (true) {
				chrctr = str[pos];

				if (chrctr === undefined) { // ( End of string reached.)
					pushComponent();
					pushComponentArray();
					return listArray;
				} else if (inComment) {
					if ((chrctr === "*") && (str[pos + 1] === "/")) { // (At end of a comment.)
						inComment = false;
						pos += 2;
						pushComponent();
						continue;
					} else {
						pos += 1; // (Skip all characters inside comments.)
						continue;
					}
				} else if (isSpace(chrctr)) {
					// (If previous character in loop was also a space, or if
					// at the beginning of the string, do not add space char to
					// component.)
					if ((str[pos - 1] && isSpace(str[pos - 1])) || (!component)) {
						pos += 1;
						continue;
					} else if (parenDepth === 0) {
						pushComponent();
						pos +=1;
						continue;
					} else {
						// (Replace any space character with a plain space for legibility.)
						chrctr = " ";
					}
				} else if (chrctr === "(") {
					parenDepth += 1;
				} else if (chrctr === ")") {
					parenDepth -= 1;
				} else if (chrctr === ",") {
					pushComponent()
					pushComponentArray();
					pos += 1;
					continue;
				} else if ((chrctr === "/") && (str[pos + 1] === "*")) {
					inComment = true;
					pos += 2;
					continue;
				}

				component = component + chrctr;
				pos += 1;
			}
		}

		function isValidNonNegativeSourceSizeValue(s) {
			if (regexCssLengthWithUnits.test(s) && (parseFloat(s) >= 0)) {return true;}
			if (regexCssCalc.test(s)) {return true;}
			// ( http://www.w3.org/TR/CSS2/syndata.html#numbers says:
			// "-0 is equivalent to 0 and is not a negative number." which means that
			// unitless zero and unitless negative zero must be accepted as special cases.)
			if ((s === "0") || (s === "-0") || (s === "+0")) {return true;}
			return false;
		}

		// When asked to parse a sizes attribute from an element, parse a
		// comma-separated list of component values from the value of the element's
		// sizes attribute (or the empty string, if the attribute is absent), and let
		// unparsed sizes list be the result.
		// http://dev.w3.org/csswg/css-syntax/#parse-comma-separated-list-of-component-values

		unparsedSizesList = parseComponentValues(strValue);
		unparsedSizesListLength = unparsedSizesList.length;

		// For each unparsed size in unparsed sizes list:
		for (i = 0; i < unparsedSizesListLength; i++) {
			unparsedSize = unparsedSizesList[i];

			// 1. Remove all consecutive <whitespace-token>s from the end of unparsed size.
			// ( parseComponentValues() already omits spaces outside of parens. )

			// If unparsed size is now empty, that is a parse error; continue to the next
			// iteration of this algorithm.
			// ( parseComponentValues() won't push an empty array. )

			// 2. If the last component value in unparsed size is a valid non-negative
			// <source-size-value>, let size be its value and remove the component value
			// from unparsed size. Any CSS function other than the calc() function is
			// invalid. Otherwise, there is a parse error; continue to the next iteration
			// of this algorithm.
			// http://dev.w3.org/csswg/css-syntax/#parse-component-value
			lastComponentValue = unparsedSize[unparsedSize.length - 1];

			if (isValidNonNegativeSourceSizeValue(lastComponentValue)) {
				size = lastComponentValue;
				unparsedSize.pop();
			} else {
				continue;
			}

			// 3. Remove all consecutive <whitespace-token>s from the end of unparsed
			// size. If unparsed size is now empty, return size and exit this algorithm.
			// If this was not the last item in unparsed sizes list, that is a parse error.
			if (unparsedSize.length === 0) {
				return size;
			}

			// 4. Parse the remaining component values in unparsed size as a
			// <media-condition>. If it does not parse correctly, or it does parse
			// correctly but the <media-condition> evaluates to false, continue to the
			// next iteration of this algorithm.
			// (Parsing all possible compound media conditions in JS is heavy, complicated,
			// and the payoff is unclear. Is there ever an situation where the
			// media condition parses incorrectly but still somehow evaluates to true?
			// Can we just rely on the browser/polyfill to do it?)
			unparsedSize = unparsedSize.join(" ");
			if (!(pf.matchesMedia( unparsedSize ) ) ) {
				continue;
			}

			// 5. Return size and exit this algorithm.
			return size;
		}

		// If the above algorithm exhausts unparsed sizes list without returning a
		// size value, return 100vw.
		return "100vw";
	}
	// jscs: enable
	/* jshint ignore:end */

	// namespace
	pf.ns = ("pf" + new Date().getTime()).substr(0, 9);

	// srcset support test
	pf.supSrcset = "srcset" in image;
	pf.supSizes = "sizes" in image;

	// using pf.qsa instead of dom traversing does scale much better,
	// especially on sites mixing responsive and non-responsive images
	pf.selShort = "picture>img,img[srcset]";
	pf.sel = pf.selShort;
	pf.cfg = cfg;

	if ( pf.supSrcset ) {
		pf.sel += ",img[" + srcsetAttr + "]";
	}

	/**
	 * Shortcut property for `devicePixelRatio` ( for easy overriding in tests )
	 */
	pf.DPR = (DPR  || 1 );
	pf.u = units;

	// container of supported mime types that one might need to qualify before using
	pf.types =  types;

	alwaysCheckWDescriptor = pf.supSrcset && !pf.supSizes;

	pf.setSize = noop;

	/**
	 * Gets a string and returns the absolute URL
	 * @param src
	 * @returns {String} absolute URL
	 */

	pf.makeUrl = memoize(function(src) {
		anchor.href = src;
		return anchor.href;
	});

	/**
	 * Gets a DOM element or document and a selctor and returns the found matches
	 * Can be extended with jQuery/Sizzle for IE7 support
	 * @param context
	 * @param sel
	 * @returns {NodeList}
	 */
	pf.qsa = function(context, sel) {
		return context.querySelectorAll(sel);
	};

	/**
	 * Shortcut method for matchMedia ( for easy overriding in tests )
	 * wether native or pf.mMQ is used will be decided lazy on first call
	 * @returns {boolean}
	 */
	pf.matchesMedia = function() {
		if ( window.matchMedia && (matchMedia( "(min-width: 0.1em)" ) || {}).matches ) {
			pf.matchesMedia = function( media ) {
				return !media || ( matchMedia( media ).matches );
			};
		} else {
			pf.matchesMedia = pf.mMQ;
		}

		return pf.matchesMedia.apply( this, arguments );
	};

	/**
	 * A simplified matchMedia implementation for IE8 and IE9
	 * handles only min-width/max-width with px or em values
	 * @param media
	 * @returns {boolean}
	 */
	pf.mMQ = function( media ) {
		return media ? evalCSS(media) : true;
	};

	/**
	 * Returns the calculated length in css pixel from the given sourceSizeValue
	 * http://dev.w3.org/csswg/css-values-3/#length-value
	 * intended Spec mismatches:
	 * * Does not check for invalid use of CSS functions
	 * * Does handle a computed length of 0 the same as a negative and therefore invalid value
	 * @param sourceSizeValue
	 * @returns {Number}
	 */
	pf.calcLength = function( sourceSizeValue ) {

		var value = evalCSS(sourceSizeValue, true) || false;
		if (value < 0) {
			value = false;
		}

		return value;
	};

	/**
	 * Takes a type string and checks if its supported
	 */

	pf.supportsType = function( type ) {
		return ( type ) ? types[ type ] : true;
	};

	/**
	 * Parses a sourceSize into mediaCondition (media) and sourceSizeValue (length)
	 * @param sourceSizeStr
	 * @returns {*}
	 */
	pf.parseSize = memoize(function( sourceSizeStr ) {
		var match = ( sourceSizeStr || "" ).match(regSize);
		return {
			media: match && match[1],
			length: match && match[2]
		};
	});

	pf.parseSet = function( set ) {
		if ( !set.cands ) {
			set.cands = parseSrcset(set.srcset, set);
		}
		return set.cands;
	};

	/**
	 * returns 1em in css px for html/body default size
	 * function taken from respondjs
	 * @returns {*|number}
	 */
	pf.getEmValue = function() {
		var body;
		if ( !eminpx && (body = document.body) ) {
			var div = document.createElement( "div" ),
				originalHTMLCSS = docElem.style.cssText,
				originalBodyCSS = body.style.cssText;

			div.style.cssText = baseStyle;

			// 1em in a media query is the value of the default font size of the browser
			// reset docElem and body to ensure the correct value is returned
			docElem.style.cssText = fsCss;
			body.style.cssText = fsCss;

			body.appendChild( div );
			eminpx = div.offsetWidth;
			body.removeChild( div );

			//also update eminpx before returning
			eminpx = parseFloat( eminpx, 10 );

			// restore the original values
			docElem.style.cssText = originalHTMLCSS;
			body.style.cssText = originalBodyCSS;

		}
		return eminpx || 16;
	};

	/**
	 * Takes a string of sizes and returns the width in pixels as a number
	 */
	pf.calcListLength = function( sourceSizeListStr ) {
		// Split up source size list, ie ( max-width: 30em ) 100%, ( max-width: 50em ) 50%, 33%
		//
		//                           or (min-width:30em) calc(30% - 15px)
		if ( !(sourceSizeListStr in sizeLengthCache) || cfg.uT ) {
			var winningLength = pf.calcLength( parseSizes( sourceSizeListStr ) );

			sizeLengthCache[ sourceSizeListStr ] = !winningLength ? units.width : winningLength;
		}

		return sizeLengthCache[ sourceSizeListStr ];
	};

	/**
	 * Takes a candidate object with a srcset property in the form of url/
	 * ex. "images/pic-medium.png 1x, images/pic-medium-2x.png 2x" or
	 *     "images/pic-medium.png 400w, images/pic-medium-2x.png 800w" or
	 *     "images/pic-small.png"
	 * Get an array of image candidates in the form of
	 *      {url: "/foo/bar.png", resolution: 1}
	 * where resolution is http://dev.w3.org/csswg/css-values-3/#resolution-value
	 * If sizes is specified, res is calculated
	 */
	pf.setRes = function( set ) {
		var candidates;
		if ( set ) {

			candidates = pf.parseSet( set );

			for ( var i = 0, len = candidates.length; i < len; i++ ) {
				setResolution( candidates[ i ], set.sizes );
			}
		}
		return candidates;
	};

	pf.setRes.res = setResolution;

	pf.applySetCandidate = function( candidates, img ) {
		if ( !candidates.length ) {return;}
		var candidate,
			i,
			j,
			length,
			bestCandidate,
			curSrc,
			curCan,
			isSameSet,
			candidateSrc,
			abortCurSrc;

		var imageData = img[ pf.ns ];
		var dpr = pf.DPR;

		curSrc = imageData.curSrc || img[curSrcProp];

		curCan = imageData.curCan || setSrcToCur(img, curSrc, candidates[0].set);

		// if we have a current source, we might either become lazy or give this source some advantage
		if ( curCan && curCan.set === candidates[ 0 ].set ) {

			// if browser can abort image request and the image has a higher pixel density than needed
			// and this image isn't downloaded yet, we skip next part and try to save bandwidth
			abortCurSrc = (supportAbort && !img.complete && curCan.res - 0.1 > dpr);

			if ( !abortCurSrc ) {
				curCan.cached = true;

				// if current candidate is "best", "better" or "okay",
				// set it to bestCandidate
				if ( curCan && isSameSet && curCan.res >= dpr ) {
					bestCandidate = curCan;
				}
			}
		}

		if ( !bestCandidate ) {

			candidates.sort( ascendingSort );

			length = candidates.length;
			bestCandidate = candidates[ length - 1 ];

			for ( i = 0; i < length; i++ ) {
				candidate = candidates[ i ];
				if ( candidate.res >= dpr ) {
					j = i - 1;

					// we have found the perfect candidate,
					// but let's improve this a little bit with some assumptions ;-)
					if (candidates[ j ] &&
						(abortCurSrc || curSrc !== pf.makeUrl( candidate.url )) &&
						chooseLowRes(candidates[ j ].res, candidate.res, dpr, candidates[ j ].cached)) {

						bestCandidate = candidates[ j ];

					} else {
						bestCandidate = candidate;
					}
					break;
				}
			}
		}

		if ( bestCandidate ) {

			candidateSrc = pf.makeUrl( bestCandidate.url );

			imageData.curSrc = candidateSrc;
			imageData.curCan = bestCandidate;

			if ( candidateSrc !== curSrc ) {
				pf.setSrc( img, bestCandidate );
			}
			pf.setSize( img );
		}
	};

	pf.setSrc = function( img, bestCandidate ) {
		var origWidth;
		img.src = bestCandidate.url;

		// although this is a specific Safari issue, we don't want to take too much different code paths
		if ( bestCandidate.set.type === "image/svg+xml" ) {
			origWidth = img.style.width;
			img.style.width = (img.offsetWidth + 1) + "px";

			// next line only should trigger a repaint
			// if... is only done to trick dead code removal
			if ( img.offsetWidth + 1 ) {
				img.style.width = origWidth;
			}
		}
	};

	pf.getSet = function( img ) {
		var i, set, supportsType;
		var match = false;
		var sets = img [ pf.ns ].sets;

		for ( i = 0; i < sets.length && !match; i++ ) {
			set = sets[i];

			if ( !set.srcset || !pf.matchesMedia( set.media ) || !(supportsType = pf.supportsType( set.type )) ) {
				continue;
			}

			if ( supportsType === "pending" ) {
				set = supportsType;
			}

			match = set;
			break;
		}

		return match;
	};

	pf.parseSets = function( element, parent, options ) {
		var srcsetAttribute, imageSet, isWDescripor, srcsetParsed;

		var hasPicture = parent && parent.nodeName.toUpperCase() === "PICTURE";
		var imageData = element[ pf.ns ];

		if ( imageData.src === undefined || options.src ) {
			imageData.src = getImgAttr.call( element, "src" );
			if ( imageData.src ) {
				setImgAttr.call( element, srcAttr, imageData.src );
			} else {
				removeImgAttr.call( element, srcAttr );
			}
		}

		if ( imageData.srcset === undefined || options.srcset || !pf.supSrcset || element.srcset ) {
			srcsetAttribute = getImgAttr.call( element, "srcset" );
			imageData.srcset = srcsetAttribute;
			srcsetParsed = true;
		}

		imageData.sets = [];

		if ( hasPicture ) {
			imageData.pic = true;
			getAllSourceElements( parent, imageData.sets );
		}

		if ( imageData.srcset ) {
			imageSet = {
				srcset: imageData.srcset,
				sizes: getImgAttr.call( element, "sizes" )
			};

			imageData.sets.push( imageSet );

			isWDescripor = (alwaysCheckWDescriptor || imageData.src) && regWDesc.test(imageData.srcset || "");

			// add normal src as candidate, if source has no w descriptor
			if ( !isWDescripor && imageData.src && !getCandidateForSrc(imageData.src, imageSet) && !imageSet.has1x ) {
				imageSet.srcset += ", " + imageData.src;
				imageSet.cands.push({
					url: imageData.src,
					d: 1,
					set: imageSet
				});
			}

		} else if ( imageData.src ) {
			imageData.sets.push( {
				srcset: imageData.src,
				sizes: null
			} );
		}

		imageData.curCan = null;
		imageData.curSrc = undefined;

		// if img has picture or the srcset was removed or has a srcset and does not support srcset at all
		// or has a w descriptor (and does not support sizes) set support to false to evaluate
		imageData.supported = !( hasPicture || ( imageSet && !pf.supSrcset ) || isWDescripor );

		if ( srcsetParsed && pf.supSrcset && !imageData.supported ) {
			if ( srcsetAttribute ) {
				setImgAttr.call( element, srcsetAttr, srcsetAttribute );
				element.srcset = "";
			} else {
				removeImgAttr.call( element, srcsetAttr );
			}
		}

		if (imageData.supported && !imageData.srcset && ((!imageData.src && element.src) ||  element.src !== pf.makeUrl(imageData.src))) {
			if (imageData.src === null) {
				element.removeAttribute("src");
			} else {
				element.src = imageData.src;
			}
		}

		imageData.parsed = true;
	};

	pf.fillImg = function(element, options) {
		var imageData;
		var extreme = options.reselect || options.reevaluate;

		// expando for caching data on the img
		if ( !element[ pf.ns ] ) {
			element[ pf.ns ] = {};
		}

		imageData = element[ pf.ns ];

		// if the element has already been evaluated, skip it
		// unless `options.reevaluate` is set to true ( this, for example,
		// is set to true when running `picturefill` on `resize` ).
		if ( !extreme && imageData.evaled === evalId ) {
			return;
		}

		if ( !imageData.parsed || options.reevaluate ) {
			pf.parseSets( element, element.parentNode, options );
		}

		if ( !imageData.supported ) {
			applyBestCandidate( element );
		} else {
			imageData.evaled = evalId;
		}
	};

	pf.setupRun = function() {
		if ( !alreadyRun || isVwDirty || (DPR !== window.devicePixelRatio) ) {
			updateMetrics();
		}
	};

	// If picture is supported, well, that's awesome.
	if ( window.HTMLPictureElement ) {
		picturefill = noop;
		pf.fillImg = noop;
	} else {

		 // Set up picture polyfill by polling the document
		(function() {
			var isDomReady;
			var regReady = window.attachEvent ? /d$|^c/ : /d$|^c|^i/;

			var run = function() {
				var readyState = document.readyState || "";

				timerId = setTimeout(run, readyState === "loading" ? 200 :  999);
				if ( document.body ) {
					pf.fillImgs();
					isDomReady = isDomReady || regReady.test(readyState);
					if ( isDomReady ) {
						clearTimeout( timerId );
					}

				}
			};

			var timerId = setTimeout(run, document.body ? 9 : 99);

			// Also attach picturefill on resize and readystatechange
			// http://modernjavascript.blogspot.com/2013/08/building-better-debounce.html
			var debounce = function(func, wait) {
				var timeout, timestamp;
				var later = function() {
					var last = (new Date()) - timestamp;

					if (last < wait) {
						timeout = setTimeout(later, wait - last);
					} else {
						timeout = null;
						func();
					}
				};

				return function() {
					timestamp = new Date();

					if (!timeout) {
						timeout = setTimeout(later, wait);
					}
				};
			};

			var onResize = function() {
				isVwDirty = true;
				pf.fillImgs();
			};

			on( window, "resize", debounce(onResize, 99 ) );
			on( document, "readystatechange", run );

			types[ "image/webp" ] = detectTypeSupport("image/webp", "data:image/webp;base64,UklGRkoAAABXRUJQVlA4WAoAAAAQAAAAAAAAAAAAQUxQSAwAAAABBxAR/Q9ERP8DAABWUDggGAAAADABAJ0BKgEAAQADADQlpAADcAD++/1QAA==" );
		})();
	}

	pf.picturefill = picturefill;
	//use this internally for easy monkey patching/performance testing
	pf.fillImgs = picturefill;
	pf.teardownRun = noop;

	/* expose methods for testing */
	picturefill._ = pf;

	window.picturefillCFG = {
		pf: pf,
		push: function(args) {
			var name = args.shift();
			if (typeof pf[name] === "function") {
				pf[name].apply(pf, args);
			} else {
				cfg[name] = args[0];
				if (alreadyRun) {
					pf.fillImgs( { reselect: true } );
				}
			}
		}
	};

	while (setOptions && setOptions.length) {
		window.picturefillCFG.push(setOptions.shift());
	}

	/* expose picturefill */
	window.picturefill = picturefill;

	/* expose picturefill */
	if ( typeof module === "object" && typeof module.exports === "object" ) {
		// CommonJS, just export
		module.exports = picturefill;
	} else if ( typeof define === "function" && define.amd ) {
		// AMD support
		define( "picturefill", function() { return picturefill; } );
	}

} )( window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "presentation",
		target = '.presentation__slides'

	function Plugin ( element, options ) {
			this.$el = $(element);
			this.$controls = $('.presentation__controls');

			this.$children = this.$el.children();
			this.settings = $.extend( {}, options, this.$el.data() );
			this._name = pluginName;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				// this.$controls.slick({
				// 	asNavFor: this.$el
				// })
				this.$el.slick({
					// options
					adaptiveHeight: false,
					dots: true,
					appendDots: this.$controls,
	  				customPaging: function(slider, i) {
	                    return '<div class="md-show">'+slider.$slides.eq(i).find('h1').text()+'</div>';
	                    // return '<button type="button" data-role="none" role="button" aria-required="false" tabindex="0">' + (i + 1) + '</button>';
	                },
					centerMode: true,
					centerPadding: 0,
					arrows: false
				});
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};

	registerplugin(target, pluginName)

})( jQuery, window, document );


//  $('.slider-for').slick({
//   slidesToShow: 1,
//   slidesToScroll: 1,
//   arrows: false,
//   fade: true,
//   asNavFor: '.slider-nav'
// });
// $('.slider-nav').slick({
//   slidesToShow: 3,
//   slidesToScroll: 1,
//   asNavFor: '.slider-for',
//   dots: true,
//   centerMode: true,
//   focusOnSelect: true
// });
//        
;
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "readmore",
		target = '.readmore',
		defaults = {
			state: 'is-inactive',
		};

	function Plugin ( element, options ) {
		this.$el = $(element);
		this.settings = $.extend( {}, defaults, options, this.$el.data() );
		this.init();
	}
	$.extend(Plugin.prototype, {
		init: function() {
			this.origHeight = this.$el.outerHeight();

			this.$el
				.addClass(this.settings.state)
				.height(this.$el.outerHeight());

			this.addEventlisteners();
		},
		addEventlisteners: function() {
			this.$el.one('click', this.toggle.bind(this));
		},
		toggle: function(e) {
			this.$el.toggleClass(this.settings.state);
			this.$el.height(this.origHeight);
		}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
		return this.each(function() {
			if ( !$.data( this, "plugin_" + pluginName ) ) {
				$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
			}
		});
	};

	registerplugin(target, pluginName);

})( jQuery, window, document );
;(function ($, window, document, undefined ) {
	"use strict";
	var	pluginName = "responsive",
		target = ".poster"

	function Plugin( element, options ) {
		//If current breakpoint is unknown, get it
		//First get the current breakpoint by triggering a resize event
		//I know, I know... weird and it needs to be refactored, but hey.
		if(document.currMedia == undefined) {
			var tag = window.getComputedStyle(document.body,':after').getPropertyValue('content');
				tag = tag.replace( /["']/g,'');
			document.currMedia = tag;
		}
		this.$el = $(element);
		this.settings = $.extend( {}, options, this.$el.data() );
		this.addEvents();
		this.load();
	}
	$.extend(Plugin.prototype, {
		addEvents: function() {
			$(window).on("Katoen:QueryEvent", $.proxy(this.load, this))
		},
		destroy: function() {
			$(window).off("Katoen:QueryEvent", $.proxy(this.load, this))

			//Remove the video element if it exists to stop loading
			this.$el.find('video').remove();
			instance = null;
		},

		getSrc: function(bp) {
			var breakpoints = ['xs', 'sm', 'md', 'lg', 'xl'],
				img = this.$el.data('src-'+bp) || this.$el.data('src');

			//Image found
			if (img) {
				return img;
			} else {
				//Get current bp index
				var bpIndex = breakpoints.indexOf(bp),
					img;
				for (var i = 0, l = breakpoints.length; i < l; i++) {
					//Find next image in line, if not found; use previous one
					//This will make sure the largest breakpoint has the latest image
					var img = this.$el.data('src-'+breakpoints[i]) || img;
					//Image is found at a next breakpoint (no xs will find md image, for example)
					//This will make sure a XS breakpoint will load in the smallest
					//image
					if (img && i >= bpIndex) {
						break;
					}
				};
				return img;
			}
		},
		load: function() {
			//VIDEO OR IMAGE IS POSSIBLE
			var newSrc = this.getSrc(document.currMedia);
			//TODO: Test for autoplay/video capability instead of sniffing for device
			//First check if there's an array (which means video). If so, test for 'mobile' to actually load an image
			if(typeof newSrc !== 'string' && (/iPhone|iPod|iPad|Android|BlackBerry/).test(navigator.userAgent)) {
				newSrc = this.$el.data('src-poster-'+document.currMedia);
			}
			//No (new) image to load? ABORT ABORT ABORT!
			var _bgImg = this.$el.css('backgroundImage');
			if(this._oldSrc == undefined && (_bgImg != 'none' && _bgImg != '')) {
				var sameImg = new RegExp(RegExp.escape(newSrc)).test(_bgImg)
			}

			if(!newSrc || this._oldSrc == newSrc || sameImg) {return;}

			//Store new image source so we can compare it
			this._oldSrc = newSrc

			//At this point, the image is probably in view, and needs to be (pre)loaded.
			this.$el.addClass('is-loading');
			
			//Array with video sources, load video
			if(typeof newSrc !== 'string') {
				// var _src = '<video class="poster__video" autoplay loop muted poster="'+this.$el.data('src-poster-'+document.currMedia)+'">';
				// var _src = '<video class="poster__video" autoplay loop muted poster="/static/images/video_poster.jpg">';
				var _src = '<video class="poster__video" autoplay loop muted poster="/static/images/transparent.gif">';
				for (var i = newSrc.length - 1; i >= 0; i--) {
					_src += '<source src="'+newSrc[i]+'" type="video/'+newSrc[i].substr(newSrc[i].lastIndexOf('.') + 1)+'"></source>';
				};
				_src += '</video>';

				this.$el
					.html(_src)
					.addClass('is-loaded')
					.css({backgroundImage: null})
			} else {
				this.$el.find('video').remove();
				var $img = $('<img/>').attr('src', newSrc).load($.proxy(function(e) {
					$img.remove(); //prevent memory leaks

					this.$el
						.css({
							backgroundImage: 'url("'+newSrc+'")'
						})
						.addClass('is-loaded');

					this.$el.trigger({
						type: "Katoen:ResponsiveImageLoaded",
						img: $img,
						width: e.target.width,
						height: e.target.height
					});

				},this));
			}
		}
	});


	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};
	registerplugin(target, pluginName)

})( jQuery, window, document );


;(function ( $, window, document, undefined ) {
	// Create the defaults once
	var pluginName = "scroggler",
		_ticking = false,
		_latestKnownScrollY = 0,
		defaults = {
			className: "is-sticky",
			fixFrom: 'auto',
			fixTo: undefined,
			beforeToggle: function() {}
		};

	// The actual plugin constructor
	function Plugin( el, options ) {
		this.$el = $(el);
		
		this.options = $.extend( {}, defaults, options) ;

		this._defaults = defaults;
		this._name = pluginName;

		this.init();
	}

	Plugin.prototype = {
		init: function() {
			if(this.options.fixFrom === 'auto') {
				$(window)
					.one('load', this.fixFrom.bind(this, this.$el.offset().top))
					.one('load', function() { $(window).trigger('scroll') });
			} else if(this.options.fixFrom < 0) {
				$(window).one('load', function() {$(window).trigger('scroll')})
			}
			$(window).on('Katoen:ScrollEvent', function(e) { this.toggleSticky(e.latestKnownScroll.top, e.latestKnownScroll.bottom) }.bind(this));
		},
		toggleSticky: function(top, bottom) {
			//Makes no sense to toggle if fixfrom is still auto.
			if(this.options.fixFrom != 'auto') {
				var	leave = top > this.options.fixTo  //+ this.options.offset;
				var enter = top > this.options.fixFrom && !leave // - this.options.offset,
				if (typeof this.options.className === 'string') {
					this.$el.toggleClass(this.options.className, enter && leave);
				} else {
					this.$el.toggleClass(this.options.className.enter, enter);
					this.$el.toggleClass(this.options.className.leave, leave);
				}
			} 
		},

		fixFrom: function(val) {
			if(val) {
				this.options.fixFrom = val;
				return this.$el;
			} else {
				return this.options.fixFrom;
			}
		}
	};
	$.fn[pluginName] = function ( options ) {
		var args = arguments;
		if (options === undefined || typeof options === 'object') {
			return this.each(function () {
				if (!$.data(this, 'plugin_' + pluginName)) {
					$.data(this, 'plugin_' + pluginName, new Plugin( this, options ));
				}
			});
		} else if (typeof options === 'string') {
			var returns;
			this.each(function () {
				var instance = $.data(this, 'plugin_' + pluginName);
				if (instance instanceof Plugin && typeof instance[options] === 'function') {
					returns = instance[options].apply( instance, Array.prototype.slice.call( args, 1 ) );
				} else {
					returns = console.error("No such method",options,"for",pluginName);		
				}
				if (options === 'destroy') {
				  $.data(this, 'plugin_' + pluginName, null);
				}
			});
			return returns !== undefined ? returns : this;
		}
	};
})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "special",
		defaults = {},
		target = '.js-special';
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.settings = $.extend( {}, options, this.$el.data() );
			this._name = pluginName;
			this._defaults 	= defaults;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				this.$el.children().each(function(i, elem) {
					var fixFrom = $(elem).offset().top
						fixFrom = fixFrom <= 100 ? 0 : fixFrom
					$(elem).scroggler({
						className: {
							enter: 'is-entered',
							leave: 'has-entered'
						},
						fixFrom: $(this).offset().top - 61,
						fixTo: $(this).offset().top + $(this).height() - 61,
					});
				});
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};

	registerplugin(target, pluginName);

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "toggle",
		target = '.js-toggle',
		defaults = {
			state: 'is-active'
		};
		
	function Plugin ( element, options ) {
		this.$el = $(element);
		this.settings = $.extend( {}, defaults, options, this.$el.data() );

		this.$target = $(this.settings.target || this.$el);
		//Test selector for 'this', so we can traverse the DOM in the DOM
		if(/this/.test(this.settings.target)) {
			var sub = this.settings.target.substring(5);
			this.$target = this.$el[sub]();
		}
		this._name = pluginName;
		
		this.init();
	}
	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function (e) {
				this.addEventlisteners();
				this.toggle();
			},
			addEventlisteners: function() {
				this.$el.on('click', this.toggle.bind(this));
			},
			toggle: function(e) {
				this.$target.toggleClass(this.settings.state);
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
		return this.each(function() {
			if ( !$.data( this, "plugin_" + pluginName ) ) {
				$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
			}
		});
	};

	delegateplugin(target, pluginName);

})( jQuery, window, document );
;(function ( $, window, document, undefined ) {
	"use strict";
	var pluginName = "video",
		target = '.video[data-src]';
		
	function Plugin ( element, options ) {
			this.$el = $(element);
			this.settings = $.extend( {}, options, this.$el.data() );
			this._name = pluginName;
			this.init();
	}

	// Avoid Plugin.prototype conflicts
	$.extend(Plugin.prototype, {
			init: function () {
				this.addEventlisteners()
			},
			addEventlisteners: function() {
				this.$el.on('click', this.insertIframe.bind(this));
			},
			insertIframe: function() {
				this.$el.prepend('<iframe src="'+this.settings.src+'?&autoplay=1"></iframe>')
			}
	});

	// A really lightweight plugin wrapper around the constructor,
	// preventing against multiple instantiations
	$.fn[ pluginName ] = function ( options ) {
			return this.each(function() {
					if ( !$.data( this, "plugin_" + pluginName ) ) {
							$.data( this, "plugin_" + pluginName, new Plugin( this, options ) );
					}
			});
	};

	registerplugin(target, pluginName);

})( jQuery, window, document );
;(function($, window, document, undefined) {
	var resizeTimeout, //Store this variable so we can reset it inside of a function
		_animRunning = false,
		_height = $(window).height(),
		_width = $(window).width(),
		_prevTop = 0, //Previous top to compare with the new top position
		//store latest known position
		latestKnownScroll = {
			top: 0,
			bottom: _height
		};

// *******************************************************************************
// * RESIZE EVENT PERF OPTIMISATIONS USING TIMEOUT (not recal frame)
// *******************************************************************************
	//Add handlers
	$(window)
		.on('scroll', scrollThrottler)
		.on('resize',resizeThrottler)
		.on("Katoen:ResizeEvent", function(e) {
			_height = e.height;
			_width = e.width;
		});

	function resizeThrottler() {
		//Resets the timeout and start over with the delay
	  	window.clearTimeout(resizeTimeout);
		// ignore resize events as long as an actualResizeHandler execution is in the queue
		resizeTimeout = setTimeout(function() {
			//Delay even more with requestanimationframe delay
			if (_animRunning) return;
			_animRunning = true;
			window.requestAnimationFrame(actualResizeHandler);
			// The actualResizeHandler will execute at a rate of 3,5fps
		}, 244);
	}

	function actualResizeHandler() {
		var query = false;
		//Stores current media query in a variable
		document.currMedia = function() {
			var tag = window.getComputedStyle(document.body,':after').getPropertyValue('content'),
				tag = tag.replace( /["']/g,'');
				
			if(tag != document.currMedia) {	query = true; }
			return tag;
		}();
		//Changed breakpoint, trigger queryevent
		if(query) {
			$(window).trigger({
				type: "Katoen:QueryEvent",
				query: document.currMedia
			});
		}
		// handle the resize event
		//Prevents multiple resizeevents firing
		$(window).trigger({
			type: "Katoen:ResizeEvent", 
			height: _height,
			width: _width 
		});
		_animRunning = false;
	};
// *******************************************************************************
// * SCROLL EVENT PERF OPTIMISATIONS
// *******************************************************************************
	// POLYFILL FOR REQUESTANIMATIONFRAME BY PAUL IRISH
	// Found here: http://www.paulirish.com/2011/requestanimationframe-for-smart-animating/
	if (!Date.now)
		Date.now = function() { return new Date().getTime(); };

	(function() {
		var vendors = ['webkit', 'moz'];
		for (var i = 0; i < vendors.length && !window.requestAnimationFrame; ++i) {
			var vp = vendors[i];
			window.requestAnimationFrame = window[vp+'RequestAnimationFrame'];
			window.cancelAnimationFrame = (window[vp+'CancelAnimationFrame']
									   || window[vp+'CancelRequestAnimationFrame']);
		}
		if (/iP(ad|hone|od).*OS 6/.test(window.navigator.userAgent) // iOS6 is buggy
			|| !window.requestAnimationFrame || !window.cancelAnimationFrame) {
			var lastTime = 0;
			window.requestAnimationFrame = function(callback) {
				var now = Date.now();
				var nextTime = Math.max(lastTime + 16, now);
				return setTimeout(function() { callback(lastTime = nextTime); },
								  nextTime - now);
			};
			window.cancelAnimationFrame = clearTimeout;
		}
	}());
	// END POLYFILL FOR REQUESTANIMATIONFRAME

	function scrollThrottler(e) {
		//From: https://developer.mozilla.org/en-US/docs/Web/API/Window.scrollY
		//Store last known scroll position because we need to determine scrolldirection on paint
		latestKnownScroll.top = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
		latestKnownScroll.bottom = latestKnownScroll.top + _height;
		
		//Prevent multiple events firing
		if(_animRunning) return;
		
		_animRunning = true;
		window.requestAnimationFrame(actualScrollHandler);
		
	};

	//Allright! We're able to trigger a event
	function actualScrollHandler () {
		_direction = latestKnownScroll.top < _prevTop? "up" : "down";
		_prevTop = latestKnownScroll.top;

		$(window).trigger({
			type: "Katoen:ScrollEvent",
			latestKnownScroll: latestKnownScroll,
			direction: _direction
		});
		_animRunning = false;
	}
})(jQuery, window, document);
var FORMALIZE=function(e,t,n,r){function i(e){var t=n.createElement("b");return t.innerHTML="<!--[if IE "+e+"]><br><![endif]-->",!!t.getElementsByTagName("br").length}var s="placeholder"in n.createElement("input"),o="autofocus"in n.createElement("input"),u=i(6),a=i(7);return{go:function(){var e,t=this.init;for(e in t)t.hasOwnProperty(e)&&t[e]()},init:{disable_link_button:function(){e(n.documentElement).on("click","a.button_disabled",function(){return!1})},full_input_size:function(){if(!a||!e("textarea, input.input_full").length)return;e("textarea, input.input_full").wrap('<span class="input_full_wrap"></span>')},ie6_skin_inputs:function(){if(!u||!e("input, select, textarea").length)return;var t=/button|submit|reset/,n=/date|datetime|datetime-local|email|month|number|password|range|search|tel|text|time|url|week/;e("input").each(function(){var r=e(this);this.getAttribute("type").match(t)?(r.addClass("ie6_button"),this.disabled&&r.addClass("ie6_button_disabled")):this.getAttribute("type").match(n)&&(r.addClass("ie6_input"),this.disabled&&r.addClass("ie6_input_disabled"))}),e("textarea, select").each(function(){this.disabled&&e(this).addClass("ie6_input_disabled")})},autofocus:function(){if(o||!e(":input[autofocus]").length)return;var t=e("[autofocus]")[0];t.disabled||t.focus()},placeholder:function(){if(s||!e(":input[placeholder]").length)return;FORMALIZE.misc.add_placeholder(),e(":input[placeholder]").each(function(){if(this.type==="password")return;var t=e(this),n=t.attr("placeholder");t.focus(function(){t.val()===n&&t.val("").removeClass("placeholder_text")}).blur(function(){FORMALIZE.misc.add_placeholder()}),t.closest("form").submit(function(){t.val()===n&&t.val("").removeClass("placeholder_text")}).on("reset",function(){setTimeout(FORMALIZE.misc.add_placeholder,50)})})}},misc:{add_placeholder:function(){if(s||!e(":input[placeholder]").length)return;e(":input[placeholder]").each(function(){if(this.type==="password")return;var t=e(this),n=t.attr("placeholder");(!t.val()||t.val()===n)&&t.val(n).addClass("placeholder_text")})}}}}(jQuery,this,this.document);jQuery(document).ready(function(){FORMALIZE.go()});
/*
 * Pointer Events Polyfill: Adds support for the style attribute "pointer-events: none" to browsers without this feature (namely, IE).
 * (c) 2013, Kent Mewhort, licensed under BSD. See LICENSE.txt for details.
 */

// constructor
function PointerEventsPolyfill(options){
    // set defaults
    this.options = {
        selector: '*',
        mouseEvents: ['click','dblclick','mousedown','mouseup'],
        usePolyfillIf: function(){
            if(navigator.appName == 'Microsoft Internet Explorer')
            {
                var agent = navigator.userAgent;
                if (agent.match(/MSIE ([0-9]{1,}[\.0-9]{0,})/) != null){
                    var version = parseFloat( RegExp.$1 );
                    if(version < 11)
                      return true;
                }
            }
            return false;
        }
    };
    if(options){
        var obj = this;
        $.each(options, function(k,v){
          obj.options[k] = v;
        });
    }

    if(this.options.usePolyfillIf())
      this.register_mouse_events();
}

// singleton initializer
PointerEventsPolyfill.initialize = function(options){
    if(PointerEventsPolyfill.singleton == null)
      PointerEventsPolyfill.singleton = new PointerEventsPolyfill(options);
    return PointerEventsPolyfill.singleton;
};

// handle mouse events w/ support for pointer-events: none
PointerEventsPolyfill.prototype.register_mouse_events = function(){
    // register on all elements (and all future elements) matching the selector
    $(document).on(this.options.mouseEvents.join(" "), this.options.selector, function(e){
       if($(this).css('pointer-events') == 'none'){
             // peak at the element below
             var origDisplayAttribute = $(this).css('display');
             $(this).css('display','none');

             var underneathElem = document.elementFromPoint(e.clientX, e.clientY);

            if(origDisplayAttribute)
                $(this)
                    .css('display', origDisplayAttribute);
            else
                $(this).css('display','');

             // fire the mouse event on the element below
            e.target = underneathElem;
            $(underneathElem).trigger(e);

            return false;
        }
        return true;
    });
};





var plugins;
function registerplugin(selector, pluginname, options) {
	plugins = plugins || [];
	plugins.push([selector, pluginname, options]);
}
function delegateplugin(selector, pluginname, event, options ) {
	event = event || 'click';
	$(document).on(event, selector, function(e) {
		e.preventDefault();
		$(e.currentTarget)[pluginname](options);
	});
}

$(document).ready(function(e) {
	for (var i = plugins.length - 1; i >= 0; i--) {
		$(plugins[i][0])[plugins[i][1]](plugins[i][2]);
	};
	PointerEventsPolyfill.initialize({});
})
;
