<template>
    <el-row style="width: 100%">
        <el-card style="width: 100%;">
            <template #header>
                <h3>Evaluation Section
                    <el-popover content="help text" trigger="hover" :width="400">
                        <template #reference>
                        <el-icon style="height: 100%; margin-left: 0.5rem">
                            <QuestionFilled />
                        </el-icon>
                        </template>
                    </el-popover>
                </h3>
            </template>
            <el-row>
                <span style="padding-right: 1em;">Model Selected: <b>{{model.model_name}}</b> </span>
                <el-button
                    type="primary"
                    size="small"
                    :loading="downloading"
                    @click="this.modelDownload()">
                    <el-icon>
                        <Download />
                    </el-icon>
                </el-button> 

                <el-divider />
                <h4>Example Input</h4>
                <el-form :model="exampleInputsForm" size="large" style="width: 100%">
                    <el-form-item>
                        <el-select v-model="exampleInputsForm.sentence_id" placeholder="Select a Sentence" size="large"
                            @change = 'updateDetailedDoc'
                            style="width: 100%;">
                            <el-option  
                                v-for="doc in documentStore.getDocuments"
                                :key="doc.id"
                                :label="doc.text"
                                :value="doc.id"
                            />
                        </el-select>
                    </el-form-item>
                </el-form>

                <el-row
                    style="width: 100%"
                    v-for="(document, docIndex) in detailedSentence"
                    :key="document.id"
                >
                    <el-row
                    style="width: 100%"
                    v-for="annotation in document.annotations"
                    :key="annotation.id"
                    >
                        <el-row style="width: 100%">
                            <el-tag>Document #{{ docIndex + 1 }}</el-tag>
                            <el-tag style="margin-left: 10px" v-if="'ground_truth' in document">
                            Ground truth: {{ getLabelByID(document.ground_truth).text }}
                            </el-tag>
                        </el-row>

                        <el-row style="width: 100%; margin-top: 10px;">
                            <el-tag type="warning">Before Debugging</el-tag>
                        </el-row>

                        <el-row style="line-height: 2; margin-top: 10px">
                            <span
                                v-for="wordData in document.words"
                                :key="wordData.id"
                                :style="getWordStyle(wordData.scores[annotation.id], annotation.label)"
                            >
                                <el-popover
                                :content=" wordData.text + ': ' + wordData.scores[annotation.id].score "
                                trigger="hover"
                                >
                                    <template #reference>
                                        <span>
                                        {{ wordData.text }}
                                        </span>
                                    </template>
                                </el-popover>
                            </span>
                        </el-row>
                    </el-row>
                    <el-divider />
                </el-row>
                <el-row
                    style="width: 100%"
                    v-for="(document, docIndex) in detailedSentence"
                    :key="document.id"
                >
        
                    <el-row
                    style="width: 100%"
                    v-for="annotation in document.annotations"
                    :key="annotation.id"
                    >
                        <el-row style="width: 100%">
                            <el-tag type="warning">After Debug Training</el-tag>
                        </el-row>
                        <el-row 
                        v-if="model.model_id"
                        v-loading="loadingAnnotations"
                        style="line-height: 2; margin-top: 10px">
                            <span
                                v-for="wordData in debugTrainingSentence"
                                :style="getWordStyle({'score': wordData.score}, annotation.label)"
                            >
                                <el-popover
                                :content=" wordData.text + ': ' + wordData.score "
                                trigger="hover"
                                >
                                    <template #reference>
                                        <span>
                                        {{ wordData.text }}
                                        </span>
                                    </template>
                                </el-popover>
                            </span>
                            <span>&nbsp;</span>
                        </el-row>
                    </el-row>
                    <el-divider />
                </el-row>
            </el-row>
        </el-card>
    </el-row>
  <EvaluationTutorial
    v-model:dialog-visible="tutorialVisible"
  />
</template>

<script>
import { Back, Check, Download } from "@element-plus/icons-vue";
import { useDocumentStore } from "@/stores/document";
import { useLabelStore } from "@/stores/label";
import { useDetailedDocumentStore } from "@/stores/detailedDocument";
import { useLocalDictionaryStore } from "@/stores/dictionaryLocal";
import { useProjectStore } from "@/stores/project";
import { useWordStore } from "@/stores/word"
import { ColorSets } from "@/utilities/constants";
import ModelsApi from "@/utilities/network/model";
import ExplanationsApi from "@/utilities/network/explanations"
import { saveAs } from 'file-saver'
import EvaluationTutorial from "@/components/project/tutorial/EvaluationTutorial.vue";


export default {
    name: "DebugEvaluation",
    components: {
        Back,
        Check,
        Download,
        EvaluationTutorial
    },
    setup() {
        const documentStore = useDocumentStore();
        const detailedDocumentStore = useDetailedDocumentStore();
        const labelStore = useLabelStore();
        const localDictionaryStore = useLocalDictionaryStore();
        const projectStore = useProjectStore();
        const wordStore = useWordStore();
        return {
            documentStore,
            detailedDocumentStore,
            labelStore,
            localDictionaryStore,
            projectStore,
            wordStore,
            getLabelByID: labelStore.getLabelByID,

        };
    },
    created() {
        const promises = [];
        promises.push(this.labelStore.fetchLabels());
        promises.push(
            this.documentStore.resetState().then(() => {
                return this.localDictionaryStore.fetchDictionary(
                    this.documentStore.getDocuments[
                        this.documentStore.getdocumentInfo.curDocIndex
                    ].id
                );
            })
        );
        Promise.all(promises).then(() => {
            this.detailedDocumentStore.fetchDocument(
                this.documentStore.getDocuments[
                    this.documentStore.getdocumentInfo.curDocIndex
                ].id
            );
        });
        this.getModelDetails()
    },
    data() {
        return {
            tutorialVisible: true,
            exampleInputsForm: {
                sentence_id: ""
            },
            downloading: false,
            model: {
                model_id: "",
                model_name: ""
            },
            detailedSentence : [],
            debugTrainingSentence: [],
            loadingAnnotations: false
        }
    },
    computed: {
        getDocText() {
            console.log("calling getDocTest")
            console.log(this.exampleInputsForm.sentence_id)
            return this.detailedSentence;
        },
        documents: function() {
            console.log('inside documents function');
            console.log(this.detailedSentence);
            return this.detailedSentence;
        }
    },
    methods: {
        updateDetailedDoc(id) {
            this.loadingAnnotations = true
            const promise = []
            promise.push(this.detailedDocumentStore.fetchDocument(id));
            Promise.all(promise).then(() => {
                this.detailedSentence = [this.detailedDocumentStore.getDocument];
                this.calculateAttrsForDoc(this.detailedSentence[0].text, this.getLabelByID(this.detailedSentence[0].ground_truth).text)
                    .then((res) => { 
                        this.debugTrainingSentence = JSON.parse(res).res
                        console.log(JSON.parse(res).res)
                        this.loadingAnnotations = false
                    }).catch(e => {
                        console.log(e)
                        this.loadingAnnotations = false

                    })
            });
        },
        getModelDetails() {
            ModelsApi.list(
                this.projectStore.getProjectInfo.id
            ).then(res => {
                console.log(res.results.at(-1));
                // check for debug false flag and pick the latest model
                const model_obj = res.results.at(-1)
                this.model.model_id = model_obj['id']
                this.model.model_name = model_obj['name']
            })
        },
        modelDownload() {
            this.downloading=true
            ModelsApi.downloadModel(
                this.projectStore.getProjectInfo.id,
                this.model.model_id
            ).then(res => {
                console.log(res.length);
                const blob = new Blob([res], { type: 'application/zip' })
                saveAs(blob, 'test.zip')
                this.downloading=false
            }).catch((err) => {
                console.log(err);
                this.downloading=false
            });
        },
        str2bytes(str) {
            var bytes = new Uint8Array(str.length);
            for (var i=0; i<str.length; i++) {
                bytes[i] = str.charCodeAt(i);
            }
            return bytes;
        },

        getWordStyle(scoreAnn = 0, labelID) {
            const style = {
                padding: "3px 3px 3px 3px",
                margin: "3px 3px 3px 3px",
                fontSize: "18px",
            };
            const score = scoreAnn.score;
            const colors = ColorSets[1].colors;
            let index = -1;
            if (score <= 0.1) {
              return style;
            } else if (score <= 0.5) {
                index = 0;
            } else if (score <= 0.75) {
                index = 1;
            } else if (score <= 1) {
                index = 2;
            }
            return {
                ...style,
                ...colors[index],
            };
        },
        calculateAttrsForDoc(text, label) {
            return ExplanationsApi.getAttributeScoresForDoc(this.projectStore.getProjectInfo.id, text, label, this.model.model_id)
            .then( res => {
                console.log(res)
                return res.res
            })
        },
    },

};


</script>