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

      <el-alert v-if="generating_explanations" 
        title="Generating Explanations..." 
        type="info" 
        description="will update once the task in done"
        center show-icon 
        :closable="false"/>
      <!-- generate explanations button -->
    </el-tab-pane>
  </el-tabs>




</template>

<script>
import { Tools } from "@element-plus/icons-vue";
import { useProjectStore } from "@/stores/project";
import { ElNotification } from 'element-plus'
import ModelsApi from "@/utilities/network/model";
import ExplanationsApi from "@/utilities/network/explanations"
import { max } from "lodash";

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
      generating_explanations: false,
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
        });
    },
    huggingfaceSubmit() {
      this.$refs['huggingfaceForm'].validate((isValid) => {
        if (isValid) {
          console.log("huggingface generate explanations");
          ExplanationsApi.generateExplanations(this.projectStore.getProjectInfo.id, true, { str: this.huggingfaceForm.str })
            .then(res => {
              console.log('Here');
              console.log(res);
              this.generating_explanations=true
              this.waitForCompletion()
              ElNotification({
                title: 'Explanation Generation Started',
                message: 'Page will automatically change once task is completed',
                type: 'success',
                duration: 0,
              });
            }).catch(err => {
              if (err.response && err.response.data){
                this.$notify.error({
                  title: "Model training failed",
                  message: err.response.data
                })
              } else {
                this.$notify.error({
                  title: "Model failed to start training",
                  message: "Please try again later"
                })
              }
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
              const project = this.projectStore.getProjectInfo
              this.projectStore.reset_state()
              console.log(project.selected_model)
              console.log(res);
              this.generating_explanations=true
              this.waitForCompletion()
              ElNotification({
                title: 'Explanation Generation Started',
                message: 'Page will automatically change once task is',
                type: 'success',
                duration: 0,
              });
            }).catch(err => {
              console.log(err)
              if (err.response && err.response.data){
                this.$notify.error({
                  title: "Model training failed",
                  message: err.response.data
                })
              } else {
                this.$notify.error({
                  title: "Model failed to start training",
                  message: "Please try again later"
                })
              }
            });
        }
      });
    },
    // didFinishGeneration() {
    //   return this.$http.get(`/projects/${this.projectStore.getProjectInfo.id}/modelstatus`).then(res => {
    //     console.log("modelstatus", res)

    //     return res
    //   })
    // },
    waitForCompletion() {
      let max_iter = 10;
      let timer = setInterval(() => ExplanationsApi.didFinishGeneration(this.projectStore.getProjectInfo.id).then((res) => {
        console.log(res)
        if (max_iter < 0 || res.status == 'finished') {
          console.log('finished')
          this.$notify.success({
          title: "Success",
          message: "Model Execution had been completed",
          duration: 0,
          })
          clearInterval(timer)
          // push to next page?
          this.$router.push({ name: 'DebugLocal' });
        } else {
          console.log('Waiting for model finish message.')
          max_iter -= 1
          console.log(max_iter)
        }
      }), 1000)

  }
  },
  mounted() {
    this.getModelList();
  }
};
</script>

<style scoped>

</style>