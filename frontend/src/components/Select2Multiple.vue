<template>
  <select multiple>
    <slot></slot>
  </select>
</template>

<script>
import select2 from 'select2'
import JQuery from 'jquery'
import 'select2/dist/css/select2.min.css'
let $ = JQuery

export default {
  name: 'select2Multiple',
  props: ['options', 'value'],
  mounted: function () {
    var vm = this
    $(this.$el)
      // init select2
      .select2({ data: this.options })
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('change', function () {
        vm.$emit('input', $(this).val())
      })
  },
  watch: {
    value: function (value) {
       if ([...value].sort().join(",") !== [...$(this.$el).val()].sort().join(","))
        $(this.$el).val(value).trigger('change');
    },
    options: function (options) {
      // update options
      $(this.$el).select2({ data: options })
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
}
</script>

<style scoped>

</style>
