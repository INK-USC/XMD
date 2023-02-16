<template>
  <h3>
    Debug Overview Page
    <el-popover content="Overview of Human Debugging Phase./n Perform task and instance annotation to start debugging phase" trigger="hover" :width="400">
      <template #reference>
        <el-icon style="height: 100%; margin-left: 0.5rem">
          <QuestionFilled />
        </el-icon>
      </template>
    </el-popover>
  </h3>

  <el-button
      type="primary"
      @click="trainDebugModel()">
      Start Debug Training
  </el-button> <br />

  <el-row style="width: 100%; margin-top: 3em;">
    <span style="padding-right: 1em;">Instance Explanation</span>
    <el-button
      size="small"
      @click="() => this.$router.push({ name: 'DebugLocal' })">
      Start Annotating
    </el-button> 
    <el-progress
        style="width: 100%; margin-top: 1em;"
        :percentage="instanceAnnotationCompletionPercentage"
        :format="getInstanceProgressBarLabel"
        type="line"
        :stroke-width="30"
        text-inside
      />

  </el-row>
  <el-row style="width: 100%; margin-top: 3em;">
    <span style="padding-right: 1em;">Task Explanation</span>
    <el-button
      size="small"
      @click="() => this.$router.push({ name: 'DebugGlobal' })">
      Start Annotating
    </el-button> 
    <el-progress
        style="width: 100%; margin-top: 1em;"
        :percentage="taskAnnotationCompletionPercentage"
        :format="getTaskProgressBarLabel"
        type="line"
        :stroke-width="30"
        text-inside
      />
  </el-row>
</template>


<script>
import { QuestionFilled} from "@element-plus/icons-vue";
import { ElNotification } from 'element-plus'
import { useProjectStore } from "@/stores/project";
import { useDocumentStore } from "@/stores/document";
import { useGlobalDictionaryStore } from "@/stores/dictionaryGlobal";
import { useWordStore } from "@/stores/word";
import DebugTrainingAPI from "@/utilities/network/debugTraining"
import DocumentsApi from "@/utilities/network/document";

export default {
  name: "DebugOverview",
  components: {
    QuestionFilled,
  },
  setup() {
    const projectStore = useProjectStore();
    const documentStore = useDocumentStore();
    const globalDictionaryStore = useGlobalDictionaryStore();
    const wordStore = useWordStore();
    return {
      projectStore,
      documentStore,
      globalDictionaryStore,
      wordStore,
    };
  },
  created() {
    const promises = [];
    promises.push(this.globalDictionaryStore.fetchDictionary());
    promises.push(this.documentStore.fetchDocuments());
    promises.push(this.wordStore.resetState());

    Promise.all(promises).then(() => {
      this.wordStore.fetchDocuments();
    });
  },
  methods: {
    // get the string for progress bar
    getInstanceProgressBarLabel() {
      let documentInfo = this.documentStore.getdocumentInfo;
      return `${documentInfo.annotatedDocCount} / ${documentInfo.totalDocCount} documents annotated`;
    },
    getTaskProgressBarLabel() {
      // this.globalDictionaryStore.fetchDictionary();
      // this.wordStore.fetchDocuments();
      return `${this.globalDictionaryStore.getRows.length} / ${this.wordStore.getWordInfo.totalWordCount} documents annotated`;
    },
    fetchDebugScores(docID) {
      return DocumentsApi.detailedDocument(
        this.projectStore.getProjectInfo.id,
        docID
      ).then((res) => {
        console.log(res);
        console.log(res.words);
        for (let word of res.words) {
          console.log("word:", word.text);
          console.log("initial score:", word.word_annotation_score[0].score);
        //   // console.log("word:", word.text, "debug score:", word.word_debug_annotation_score.score)
        }
      })
    },
    trainDebugModel() {
      DebugTrainingAPI.train(this.projectStore.getProjectInfo.id)
        .then(res => {
          console.log('Here');
          console.log(res); 
          this.waitForCompletion()
          ElNotification({
            title: 'Debug Training Started',
            message: 'Page will automatically change once task is completed',
            type: 'success',
            duration: 0,
          });
        }).catch(err => {
          // this.loadingExplanations = false
          if (err.response && err.response.data) {
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
      this.fetchDebugScores(this.documentStore.getDocuments[1].id)
    },
    waitForCompletion() {
      return
    },
  },
  computed: {
    // get the percentage of the annotation progress
    instanceAnnotationCompletionPercentage() {
      let documentInfo = this.documentStore.getdocumentInfo;
      if (documentInfo.totalDocCount == 0) {
        return 0;
      } else {
        let percentage =
          (100 * documentInfo.annotatedDocCount) / documentInfo.totalDocCount;
        return percentage;
      }
    },
    taskAnnotationCompletionPercentage() {
      let wordInfo = this.wordStore.getWordInfo;
      if (wordInfo.totalWordCount == 0) {
        return 0;
      } else {
        let percentage =
          (100 * Array.from(this.globalDictionaryStore.getRows).length) / wordInfo.totalWordCount;
        return percentage;
      }
    }
  }
};
</script>
