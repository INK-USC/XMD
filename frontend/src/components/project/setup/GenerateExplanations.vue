<template>
  <h3>Generate Explanations Page</h3>
  <!-- <el-tabs type="border-card" class="demo-tabs">
    <el-tab-pane>
      <template #label>
        <span class="custom-tabs-label">
          <el-icon><Tools /></el-icon><span>Route</span>
        </span>
      </template>
      Route
    </el-tab-pane>
    <el-tab-pane label="Huggingface">
      <el-form :model="huggingfaceForm">
        <el-form-item label="huggingface string">
          <el-input v-model="huggingfaceForm.str" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="huggingfaceSubmit">Generate Explanations</el-button>
        </el-form-item>

        
      </el-form>
    </el-tab-pane>
  </el-tabs> -->


    <el-tabs type="border-card">
      <el-tab-pane label="Huggingface">
        <el-form :model="huggingfaceForm" ref="huggingfaceForm" :rules="huggingfaceForm.rules" label-position="top">
          <el-form-item label="huggingface string" prop="str">
            <el-col :span="6"><el-input v-model="huggingfaceForm.str" /></el-col>
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
              <el-option
                v-for="item in customModelForm.modelList"
                :key="item.id"
                :label="item.name"
                :value="item.name"
              />
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
      console.log('tab click')
      ModelsApi.list(this.projectStore.getProjectInfo.id)
      .then((res) => {
        this.customModelForm.modelList = res.results;
      });
    },
    huggingfaceSubmit() {
      this.$refs['huggingfaceForm'].validate((isValid) => {
        if (isValid) {
          console.log("huggingface generate explanations");
        }
      });
    },
    customModelSubmit() {
      this.$refs['customModelForm'].validate((isValid) => {
        if (isValid) {
          console.log("custom model generate explanations");
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
/* .demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.demo-tabs .custom-tabs-label .el-icon {
  vertical-align: middle;
}
.demo-tabs .custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
} */
</style>