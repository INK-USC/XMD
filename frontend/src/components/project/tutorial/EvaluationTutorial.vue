<template>
  <el-dialog
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="40%"
  >
    <span slot="title" style="font-size: 18pt; font-weight:bold">Evaluation</span>
    <div class="container">
      <div class="row" style="padding: 10px">
          <br><br>
            <p class="text" style="font-size: 15pt; text-align: justify">
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
