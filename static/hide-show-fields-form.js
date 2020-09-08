$("#seeAnotherField").change(function() {
			if ($(this).val() == "yes") {
				$('#otherFieldDiv').show();
				$('#otherField').attr('required','');
				$('#otherField').attr('data-error', 'This field is required.');
			} else {
				$('#otherFieldDiv').hide();
				$('#otherField').removeAttr('required');
				$('#otherField').removeAttr('data-error');				
			}
		});
$("#seeAnotherField").trigger("change");


$("#type").change(function() {
			if ($(this).val() == "Month") {

				$('#ByMonthDiv').show();
				$('#year').attr('required','');
				$('#year').attr('data-error', 'This field is required.');
				$('#from').attr('required','');
				$('#from').attr('data-error', 'This field is required.');
				$('#to').attr('required','');
				$('#to').attr('data-error', 'This field is required.');

				$('#ByYearDiv').hide();
				$('#FromYear').removeAttr('required');
				$("#FromYear").removeAttr('data-error');
        		$('#ToYear').removeAttr('required');
				$('#ToYear').removeAttr('data-error');
			} else {

				$('#ByYearDiv').show();
				$('#FromYear').attr('required','');
				$('#FromYear').attr('data-error', 'This field is required.');
				$('#ToYear').attr('required','');
				$('#ToYear').attr('data-error', 'This field is required.');

				$('#ByMonthDiv').hide();
				$('#year').removeAttr('required');
				$('#year').removeAttr('data-error');
        		$('#from').removeAttr('required');
				$('#from').removeAttr('data-error');
				$('#to').removeAttr('required');
				$('#to').removeAttr('data-error');
			}
		});
$("#type").trigger("change");
		