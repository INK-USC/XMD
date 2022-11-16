<template>
  <h3>Generate Explanations Page</h3>

  <el-tabs type="border-card">
    <el-tab-pane label="Huggingface">
      <el-form :model="huggingfaceForm" ref="huggingfaceForm" :rules="huggingfaceForm.rules" label-position="top">
        <el-form-item label="huggingface string" prop="str">
          <el-col :span="6">
            <el-input v-model="huggingfaceForm.str" />
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="huggingfaceSubmit">Generate Explanations</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>

    <el-tab-pane label="Custom Model">
      Custom Model
      <el-form :model="customModelForm" ref="customModelForm" :rules="customModelForm.rules" label-position="top">
        <el-form-item label="Custom Model" prop="select">
          <el-select v-model="customModelForm.select" clearable placeholder="Select Model">
            <el-option v-for="item in customModelForm.modelList" 
              :key="item.id" :label="item.name"
              :value="[item.id, item.model]" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="customModelSubmit">Generate Explanations</el-button>
        </el-form-item>
      </el-form>

      <!-- el-select dropdown -->

      <!-- generate explanations button -->
    </el-tab-pane>
  </el-tabs>




</template>

<script>
import { Tools } from "@element-plus/icons-vue";
import { useProjectStore } from "@/stores/project";
import ModelsApi from "@/utilities/network/model";
import ExplanationsApi from "@/utilities/network/explanations"

export default {
  name: "GenerateExplanations",
  components: {
    Tools,
  },
  setup() {
    const projectStore = useProjectStore();
    return {
      projectStore,
    };
  },
  data() {
    return {
      huggingfaceForm: {
        str: "",
        rules: {
          str: {
            required: true, message: 'Please input huggingface string', trigger: 'blur'
          },
        },
      },
      customModelForm: {
        modelList: [],
        select: '',
        rules: {
          select: {
            required: true, message: 'Please select model', trigger: 'change'
          },
        },
      },
    }
  },
  methods: {
    getModelList() {
      console.log('model list')
      ModelsApi.list(this.projectStore.getProjectInfo.id)
        .then((res) => {
          this.customModelForm.modelList = res.results;
          console.log(res.results);
        });
    },
    huggingfaceSubmit() {
      this.$refs['huggingfaceForm'].validate((isValid) => {
        if (isValid) {
          console.log("huggingface generate explanations");
          ExplanationsApi.generateExplanations(this.projectStore.getProjectInfo.id, true, { str: this.huggingfaceForm.str })
            .then(res => {
              console.log(res);
            });
        };
      });
    },
    customModelSubmit() {
      this.$refs['customModelForm'].validate((isValid) => {
        if (isValid) {
          console.log("custom model generate explanations");
          console.log("model_id:", this.customModelForm.select[0]);
          console.log("model_path", this.customModelForm.select[1]);
          ExplanationsApi.generateExplanations(this.projectStore.getProjectInfo.id, false, { model_id: this.customModelForm.select[0], model_path: this.customModelForm.select[1] })
            .then(res => {
              console.log(res);
            });
        }
      });
    },
  },
  mounted() {
    this.getModelList();
  }
};
</script>

<style scoped>

</style>