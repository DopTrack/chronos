/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

if ($('.nav-carousel').length && !$('.carousel__slides').length) {
    $('.nav-carousel h4').click(function () {
        $(this).parent().toggleClass('is-active');
    });
}

var tud = {
	log: function (msg, type) {
		switch(type){case 'error':case 'e':console.error(msg);break;case 'warning':case 'w':console.warn(msg);break;case 'info':case 'i':case 'notice':console.info(msg);break;default:console.log(msg);}
	},
	closest: function (elem, selector) {
		var firstChar = selector.charAt(0);
		// Get closest match
		for ( ; elem && elem !== document; elem = elem.parentNode ) {
			// If selector is a class
			if ( firstChar === '.' ) {
				if ( elem.classList.contains( selector.substr(1) ) ) {
					return elem;
				}
			}

			// If selector is an ID
			if ( firstChar === '#' ) {
				if ( elem.id === selector.substr(1) ) {
					return elem;
				}
			} 

			// If selector is a data attribute
			if ( firstChar === '[' ) {
				if ( elem.hasAttribute( selector.substr(1, selector.length - 2) ) ) {
					return elem;
				}
			}

			// If selector is a tag
			if ( elem.tagName.toLowerCase() === selector ) {
				return elem;
			}
		}
		return false;
	},
	textTransform: function(string, type) {
		var result = false;
		if(!type) type = 'firstUpper';
		switch(type) {
			case 'firstUpper':
				result = string.charAt(0).toUpperCase() + string.slice(1);
				break;
		}
		return result;
	}
}

DOMTokenList.prototype.addMany = function(classes) {
    var array = classes.split(' ');
    for (var i = 0, length = array.length; i < length; i++) {
      this.add(array[i]);
    }
}

DOMTokenList.prototype.removeMany = function(classes) {
    var array = classes.split(' ');
    for (var i = 0, length = array.length; i < length; i++) {
		this.remove(array[i]);
    }
}

var forms = {
	forbidden_password: ['password','test'],
	reg_url: /^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?$/i,
	reg_url_html5: '^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?$',
    reg_text_only: /^[a-zA-Z_\ \- \.]*$/,
    reg_text_only_dot: /^[a-zA-Z \.]*$/,
    reg_text_only_html5: '^[a-zA-Z_\ \-]*$',
	reg_password: /(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}/,
	reg_password_html5: '(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}',
	reg_search_html5: '([^\\s]*)',
	reg_email: /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,4}))$/,
	reg_email_html5: '^(([^<>()[\\]\\\\.,;:\\s@\\"]+(\\.[^<>()[\\]\\\\.,;:\\s@\\"]+)*)|(\\".+\\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,4}))$',
	id_counter:0,
	lookup:{},
	get_Type:function(type, form_id){
		var result = [];
		if(this.lookup[form_id]['type'][type]) result = this.lookup[form_id]['type'][type];
		return result;
	},
	get_Type_OBJ_SINGLE:function(type, index, form_id){
		return this.lookup[form_id]['field'][this.lookup[form_id]['type'][type][index]]['objref'];
	},
	get_Type_OBJ_ARRAY:function(type, form_id){
		var result = [],
			arr = this.get_Type(type, form_id),
			l = arr.length;
		
		if(l > 0) {while (l--) result.push(this.get_Type_OBJ_SINGLE(type, l, form_id));}

		return result;
	},
	
	removeClasses: function (el) {
		el.classList.removeMany( "input_wrong input_neutral input_required input_ok" )
	},

	field_ok:function(el) {
		this.hide_msg(el);
		p = el.parentNode;
		if (!p.classList.contains('inner')) p = p.parentNode.parentNode;
		p.classList.add('input_ok');
		el.setAttribute('aria-invalid', 'false');
	},
	show_msg:function(msg, el, label) {
		if (label) msg = ['<span class="msg_label">' + label + '</span>:',msg].join(' ');
		this.hide_msg(el);
		p = el.parentNode;
		if (!p.classList.contains('inner')) p = p.parentNode.parentNode;

		this.removeClasses(p)
		msgbox = p.parentNode.getElementsByClassName('msg')[0];
		if(msgbox) {
			el.setAttribute('aria-invalid', 'true');
			p.classList.add('input_wrong');
			msgbox.classList.add('show');
			msgbox.setAttribute('aria-hidden', 'false');
			msgbox.innerHTML = msg;
		}
	},
	hide_msg:function(el) {
		p = el.parentNode;
		if (!p.classList.contains('inner')) p = p.parentNode.parentNode;

		this.removeClasses(p);
		msgbox = p.parentNode.getElementsByClassName('msg')[0];
		if(msgbox) {
			msgbox.classList.remove('show');
			msgbox.setAttribute('aria-hidden', 'true');
			msgbox.innerHTML = '';
		}
	},
	
	formState:function(form_id, field_obj, action){
		var requiredFields = this.get_Type('required', form_id),
			emailFields = this.get_Type('email', form_id),
			urlFields = this.get_Type('url', form_id),
			i = requiredFields.length,
			k = emailFields.length,
			m = urlFields.length,
			field_id = false,
			keypress = false,
			blur = false;

		switch (action){
			case 'keypress':
				keypress = true;
				break;

			case 'blur':
				blur = true;
				break;
		}
		
		if(field_obj) {field_id = field_obj.getAttribute('id');}

		if(i > 0 || k > 0 || m > 0)
		{
			var go = true,
				objref = null,
				field_type = null,
				field_value = '';
				
// REQUIRED CHECK	
			if (i > 0) {
				while (i--) {
					objref = this.get_Type_OBJ_SINGLE('required', i, form_id);
					field_type = this.lookup[form_id]['field'][this.lookup[form_id]['type']['required'][i]]['type'];
					
					
					var continuecheck = true;


					// select tag contains a bug with selected=selected
					// http://stackoverflow.com/questions/1479233/why-doesnt-firefox-show-the-correct-default-select-option/8258154#8258154					
					switch (field_type){
						case 'datepicker':
						case 'select':
							continuecheck = false;
							break;
					}

					
					if (continuecheck) {
						switch(field_type) {
							/*
							case 'select':
								if (objref.selectedIndex && objref.options[objref.selectedIndex])
									field_value = objref.options[objref.selectedIndex].text;
								else
									field_value = 'test';
								if (field_value == '---') field_value = '';
								break;
							*/	
							default:
								field_value = objref.value;
						}

						if(!field_value) {
							var label = this.lookup[form_id]['field'][requiredFields[i]]['label'],
								go = false;
							if(!keypress && requiredFields[i] == field_id) {
								this.show_msg(' is a required field', objref, label);
							}
						} else {
							if(blur) this.field_ok(objref);
						}
					}
				}
			}
		
		
//EMAIL CHECK
			if (k > 0) {
				while (k--) {
					objref = this.get_Type_OBJ_SINGLE('email', k, form_id);
					if(objref.value){
						if(!this.reg_email.test(objref.value)) {
							go = false;
							var label = this.lookup[form_id]['field'][emailFields[k]]['label'];
							if(!keypress) this.show_msg('Fill in a correct email address', objref);
						}
					}
				}
			}
//URL CHECK
			if (m > 0) {
				while (m--) {
					objref = this.get_Type_OBJ_SINGLE('url', m, form_id);
					if(objref.value){
						if(!this.reg_url.test(objref.value)) {
							go = false;
							var label = this.lookup[form_id]['field'][urlFields[m]]['label'];
							if(!keypress) this.show_msg('Fill in a correct url', objref);
						}
					}
				}
			}

			if(go) this.lookup[form_id].submit.disabled = false; else this.lookup[form_id].submit.disabled = true;
		}
	},
	
	init : function() {
		var forms = document.getElementsByTagName("form"),
			forms_length = forms.length;
		
		if (forms_length) {
			// iterate through all the forms
			while (forms_length--) {
				var form = forms[forms_length],
					form_id = form.getAttribute('id'),
					wrong = {},
					submit = false,
					required = [],
					field_types = {},
					el = {},
					fields = form.elements,
					i = fields.length,
					lookup_label = [],
					allLabels = form.getElementsByTagName('LABEL');

					for (var i = 0; i < allLabels.length; i++) {
						if (allLabels[i].htmlFor != '') {
							lookup_label[allLabels[i].htmlFor] = [
								allLabels[i].innerHTML,
								allLabels[i]
							];
						}
					}

				if (!form_id) {
					form_id = ['f', this.id_counter].join('');
					form.setAttribute('id', form_id);
					this.id_counter ++;
				}

				li = form.querySelectorAll('form .controls');
				if(li) {
					var o = li.length;
					if(o>0)while (o--) li[o].innerHTML = '<span class="outer"><span class="inner">' + li[o].innerHTML + '</span><span class="msg" aria-hidden="true" role="alert"></span></span>';
				}
				
				if (i && fields) {
					// iterate through all the fields of a form
					while (i--) {
						var field = fields[i];
						if (field) {
							var field_tag = field.tagName.toLowerCase(),
							field_type = field_tag,
							field_class = field.getAttribute('class');
							
							if (field_class && field_class == 'text_only') field_type = 'text_only';
							
							if (field_class && field_class == 'datepicker') field_type = 'datepicker';

							else if (field_class && field_class == 'text_only_diacritics') field_type = 'text_only_diacritics';
							else if (field_type == 'input') field_type = field.getAttribute('type');

							switch(field_type) {
								case 'email':
									if (!field.getAttribute('patern')) field.setAttribute('pattern',this.reg_email_html5);
									if (!field.getAttribute('placeholder')) field.setAttribute('placeholder', 'your@email.com');
									break;
									
								case 'url':
									if (!field.getAttribute('patern')) field.setAttribute('pattern',this.reg_url_html5);
									if (!field.getAttribute('placeholder')) field.setAttribute('placeholder', 'http:// ...');
									break;

								case 'search':
									if (!field.getAttribute('placeholder')) field.setAttribute('placeholder', 'Search');
									break;
							}
							switch(field_type) {
								case 'hidden':
								case 'legend':
								case 'fieldset':
								case 'reset':
									break;

								case 'button':
									if(field.getAttribute('class') == 'submit') submit = field;
									break;

								case 'submit':
									submit = field;
									break;

								default:
									var field_id = field.getAttribute('id'),
										el_group = tud.closest(field ,'.formrow')
										label = null,
										label_for = false,
										field_label = '',
										field_required = false;

									if (field.required) field_required = field.required;

									if (el_group && el_group.classList.contains('required') && !el_group.classList.contains('group-choices')) {
										field_required = field.required = true;
									}

									if (el_group && !label) {
										var labels = el_group.getElementsByTagName("label");
										if (labels) {
											label = labels[0];
											field_label = label.innerHTML;
											label_for = label.getAttribute('for');
											if (field_id != label_for) label.setAttribute('for', field_id);
										}
									}
									
									if (!field_id) {
										field_id = ['field', this.id_counter].join('');
										field.setAttribute('id', field_id);
										this.id_counter ++;
									} else if (lookup_label[field_id]) {
										label = lookup_label[field_id][1];
										field_label = lookup_label[field_id][0];
										label_for = true;
									}

									if(!field_types[field_type]) field_types[field_type] = [];
									field_types[field_type].push(field_id);

									if(field_tag == 'input') {
										if(!field_types[field_tag]) field_types[field_tag] = [];
										field_types[field_tag].push(field_id);
									}
								
									if (field_required) {
										field.setAttribute('aria-required','true');
										if(!field_types['required']) field_types['required'] = [];
										field_types['required'].push(field_id);
									}
									
									el[field_id] = {
										'label':field_label,
										'type':field_type,
										'name':field.getAttribute('name'),
										'tag':field_tag,
										'objref':field
									};
									break;
								}

						}

						
					}
				}
				this.lookup[form_id] = {'formobj': form, 'submit': submit,'field': el, 'wrong': wrong, 'type': field_types};
				this.formState (form_id, 0);
			}
		}
		$( "select" ).wrap( '<span class="select i_outer"><span class="i_inner"></span></span>' );
	}
}

$(document).ready(function() {
	forms.init();
	for (var key in forms.lookup) {
		var inputField = forms.get_Type_OBJ_ARRAY('input', key),
			l = inputField.length;
		if(l>0) {
			while (l--) {
				var el = inputField[l];
				el.addEventListener('blur', function(){
					var form_id = tud.closest(this, 'form').getAttribute('id');
					forms.formState(form_id, this, 'blur');
				});
			
				el.addEventListener('keyup', function(e){
					if(e.keyCode != 9 && e.keyCode != 13 ) {
						var form_id = tud.closest(this, 'form').getAttribute('id');
						forms.formState(form_id, this, 'keypress');
					}
				});
			}
		}

		var selectField = forms.get_Type_OBJ_ARRAY('select', key),
			l = selectField.length;
		if(l>0) {
			while (l--) {
				var el = selectField[l];
				el.addEventListener('change', function(){
					var form_id = tud.closest(this, 'form').getAttribute('id');
					forms.formState(form_id, this, 'blur');
				});
			}
		}
	}

    $('.datepicker').datepicker({
		changeMonth:true,
		changeYear: true
	})
})
