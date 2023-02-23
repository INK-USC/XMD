<template>
  <el-dialog
    :title="'Evaluation'"
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="40%"
  >
    <div class="container">
      <div class="row">
          <br><br>
            <p class="text" style="text-align: justify">
              Now you have debugged model. <br>
              You can download the debug model. <br>
              Moreover, you can check how the explanations get changed after debugging!
            </p>
      </div>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="() => $emit('update:dialogVisible', false)">
          Understand
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>

// the form when user create/edit a project
export default {
  name: "EvaluationTutorial",
  props: { dialogVisible: Boolean, existingInfo: Object },
  setup() {
  },
  data() {
    return {};
  },
  methods: {
  },
};
</script>

<style scoped></style>
