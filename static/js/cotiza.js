function isEmptyStr(str) { return str.match(/^\s*$/); }

jQuery(function ($) {
	var $form = $('#formCotiza'), $productos = $('select[name="producto[]"]').hide();

	$form.submit(function () {
		var $inputs = $form.find('input[type="text"]');

		$inputs.each(function (index, el) {
			var $input = $(this), $group = $input.closest('.control-group');

			var $inputProds = $('.inputProd');

			if(!($input.is($inputProds.last()) && !$input.is($inputProds.first()))) {
				if($input.val().match(/^\s*$/)) {
					$group.addClass('warning');
				} else {
					$group.removeClass('warning');
				}
			}

			if(index == $inputs.size()-1) {
				var $warnings = $form.find('.warning');
				$warnings.first().find('input').focus()

				if($warnings.size() <= 0) {

					$productos.html('');

					$('.inputProd').each(function () {
						var $self = $(this);

						if(!$self.val().match(/^\s*$/)) {
							$productos.append('<option selected="selected" value="'+$self.val()+'" />');
						}
					});


					$.post($form.attr('href'), $form.serialize(), 
						function (r) {
							$form.html(r)
					})
				}
			}
		});

		return false;
	});

	var tmpl = '<div class="control-group groupProd">'+
					'<label class="control-label" for="inputProd%count">Producto %count</label>'+
					'<div class="controls">'+
					  '<input type="text" id="inputProd%count" class="inputProd" placeholder="ej. Compresor de aire">'+
					'</div>'+
				'</div>', prod_count=1;

	function format_tmpl() {
		prod_count++;

		return tmpl.replace(new RegExp('%count', 'g'), prod_count);
	}

	$('.inputProd').live('focus', function () {
		var $self = $(this), $group = $self.closest('.groupProd'), $prev = $group.prev('.groupProd');

		if($prev.size() > 0) {
			$prev = $prev.find('.inputProd');

			if(isEmptyStr($prev.val())) return $prev.focus();
		}

		if($group.next('.groupProd').size() <= 0) {
			$(format_tmpl()).insertAfter($group);
		}

	});

	$('.inputProd').live('blur', function () {
		var $self = $(this), $group = $self.closest('.groupProd'), $next = $group.next('.groupProd');

		if(isEmptyStr($self.val())) {
			$next.remove();

			prod_count--;
		}
	});
});