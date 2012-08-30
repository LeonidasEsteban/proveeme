jQuery(function ($) {

	var $concuer = $('#concuer').hide(), $regiones = $('#regiones').hide(), $success = $('#success').hide();

	function isEmptyStr(str) { return str.match(/^\s*$/); }

	function autocomProduc() {
		$( "input.producto" ).autocomplete({ source: '/buscar_producto', minLength: 2 });
	}

	function autocomReg() {
		$( "input.region" ).autocomplete({ source: '/buscar_region', minLength: 2 });
	}

	function reloadConc() {
		var vals = [], vals2 = [];

		$('input.producto').each(function () {
			var val = $(this).val();
			if(!isEmptyStr(val)) vals.push(val);
		});

		$('input.region').each(function () {
			var val = $(this).val();
			if(!isEmptyStr(val)) vals2.push(val);
		});

		$.get('/buscar_empresas', { productos: vals.join(','), regiones: vals2.join(',') }, function (r) {
			$concuer.html(r).show();
		});
	}

	var prod_count = 2, reg_count = 2;
	$('input.producto').live('focus', function () {
		var $self = $(this), $prev = $self.parent().prev('p').find('input.producto');

		if($prev.size() > 0) {
			if(isEmptyStr($prev.val())) return $prev.focus();
		}

		if($self.parent().next('p').size() <= 0) {
			$('<p><input type="text" placeholder="Producto '+prod_count+'" name="producto-'+prod_count+'" class="producto disabled" /></p>').insertAfter($self.parent());
			autocomProduc();

			prod_count++;

		}

		$self.removeClass('disabled');
	});

	autocomProduc();
	

	$('input.producto').live('blur', function () {
		var $self = $(this), $next = $self.parent().next('p').find('input.producto');

		if(isEmptyStr($self.val())) {
			$next.parent().remove();

			prod_count--;

			$self.addClass('disabled');
		} else {
			reloadConc();
		}
	});

	// reg
	$('input.region').live('focus', function () {
		var $self = $(this), $prev = $self.parent().prev('p').find('input.region');

		if($prev.size() > 0) {
			if(isEmptyStr($prev.val())) return $prev.focus();
		}

		if($self.parent().next('p').size() <= 0) {
			$('<p><input type="text" placeholder="Región '+prod_count+'" name="region-'+prod_count+'" class="region disabled" /></p>').insertAfter($self.parent());
			autocomReg();

			prod_count++;
		}

		$self.removeClass('disabled');
	});

	$('input.region').live('blur', function () {
		var $self = $(this), $next = $self.parent().next('p').find('input.region');

		if(isEmptyStr($self.val())) {
			$next.parent().remove();

			prod_count--;

			$self.addClass('disabled');
		} else {
			reloadConc();
		}
	});

	$('input.zona').change(function () {
		var $self = $(this);

		if($self.val() == 0) {
			$regiones.show();
		} else {
			$regiones.hide();
		}
	});

	$('#solic-coti').submit(function () {
		var $self = $(this);

		$success.show();
		$self.hide();

		return false;
	})
});