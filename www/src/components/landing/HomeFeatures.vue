<template>
  <!-- https://tailwindui.com/components/marketing/sections/feature-sections -->
  <div class="py-12 bg-white">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="lg:text-center">
        <h2
          class="text-base text-yellow-600 font-semibold tracking-wide uppercase"
        >
          {{ subtitle }}
        </h2>
        <p
          class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
        >
          A better way to translate products
        </p>
        <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
          We started this product from our own experience and pain points
          building multi-lingual products, so that you and your team don't have
          to suffer to provide your great products to more demographics!
        </p>
      </div>

      <div class="mt-10">
        <dl
          class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10"
        >
          <div v-for="feature in features" :key="feature.name" class="">
            <dt class="flex items-center">
              <div
                class="flex items-center justify-center h-12 w-12 rounded-md bg-yellow-600 text-white"
              >
                <component
                  :is="feature.icon"
                  class="h-6 w-6"
                  aria-hidden="true"
                />
              </div>
              <p class="ml-8 text-lg leading-6 font-medium text-gray-900">
                {{ feature.name }}
              </p>
            </dt>
            <dd class="mt-2 ml-20 text-base text-left text-gray-500">
              {{ feature.description }}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  </div>
</template>

<script>
import { onBeforeUnmount, ref } from "vue";
import shuffle from "lodash.shuffle";

import {
  AnnotationIcon,
  GlobeAltIcon,
  LightningBoltIcon,
  ScaleIcon,
} from "@heroicons/vue/outline";

const features = [
  {
    name: "No-bullshit features",
    description:
      "We have taken the core of internationalizaton and removed all the extra to provide the most streamlined experience when translating products.",
    icon: GlobeAltIcon,
  },
  {
    name: "Open Source",
    description:
      "All the code (including this very page) is open source and can be freely self-hosted. We also welcome contributions, and maintain a public roadmap.",
    icon: ScaleIcon,
  },
  {
    name: "Seamless integrations",
    description:
      "Thanks to our command line interface (CLI), you can easily integrate internationalization into your existing development workflow.",
    icon: LightningBoltIcon,
  },
  {
    name: "Private by default",
    description:
      "Besides being GDPR compliant, we offer a simple user access management, never store passwords, and your data will always be yours.",
    icon: AnnotationIcon,
  },
];

export default {
  setup() {
    const subtitles = shuffle([
      "internationalisation",
      "internacionalización",
      "internationalization",
      "अंतर्राष्ट्रीयकरण",
      "Internasionalisering",
      "Ndërkombëtarizimi",
      "ዓለም አቀፋዊነት",
      "Միջազգայնացում",
      "تدويل",
      "beynəlmiləlləşmə",
      "আন্তর্জাতিকীকরণ",
      "nazioartekotzea",
      "інтэрнацыяналізацыя",
      "internacionalizacija",
      "интернационализация",
      "နိုင်ငံတကာ",
      "internacionalització",
      "国际化",
      "國際化",
      "internacionalizace",
      "internationalisering",
      "internaciigo",
      "rahvusvahelistumine",
      "kansainvälistyminen",
      "ინტერნაციონალიზაცია",
      "Internationalisierung",
      "διεθνοποίηση",
      "આંતરરાષ્ટ્રીયકરણ",
      "entènasyonalizasyon",
      "hoʻokiwikā",
      "בִּנאוּם",
      "nemzetközivé válás",
      "alþjóðavæðing",
      "mba ozo",
      "penginternasionalan",
      "idirnáisiúnú",
      "internazionalizzazione",
      "国際化",
      "internasionalisasi",
      "ಅಂತರರಾಷ್ಟ್ರೀಕರಣ",
      "интернационалдандыру",
      "ភាវូបនីយកម្ម",
      "국제화",
      "интернационалдаштыруу",
      "ສາກົນ",
      "tincidunt",
      "internacionalizācija",
      "internacionalizacija",
      "Internationaliséierung",
      "интернационализација",
      "fanatontoloana",
      "pengantarabangsaan",
      "അന്താരാഷ്ട്രവൽക്കരണം",
      "internazzjonalizzazzjoni",
      "Whakawhitinga",
      "आंतरराष्ट्रीयकरण",
      "олон улсын",
      "अन्तर्राष्ट्रियकरण",
      "internasjonalisering",
      "ଆନ୍ତର୍ଜାତୀୟକରଣ",
      "نړیواله کول",
      "بین المللی شدن",
      "umiędzynarodowienie",
      "internacionalização",
      "ਅੰਤਰਰਾਸ਼ਟਰੀਕਰਨ",
      "internaționalizare",
      "интернационализация",
      "faʻavaomaloina",
      "eadar-nàiseantachd",
      "بين الاقوامي آبادڪاري",
      "ජාත්‍යන්තරකරණය",
      "internacionalizácia",
      "internasionalisasi",
      "kimataifa",
      "internationalisering",
      "интернатсионалӣ",
      "சர்வதேசமயமாக்கல்",
      "అంతర్జాతీయకరణ",
      "ความเป็นสากล",
      "uluslararasılaşma",
      "halkaralaşmak",
      "інтернаціоналізація",
      "عالمگیریت",
      "xalqarolashtirish",
      "quốc tế hóa",
      "rhyngwladoli",
      "ynternasjonalisaasje",
      "ukwenziwa kwehlabathi",
      "אינטערנאציאנאליזאציע",
      "agbaye",
      "ukwenziwa kwamazwe omhlaba jikelele",
    ]);

    const subtitle = ref("i18n");

    let counter = 0;
    const interval = setInterval(() => {
      subtitle.value = subtitles[counter % subtitles.length];
      counter++;
    }, 2000);

    onBeforeUnmount(() => {
      clearInterval(interval);
    });

    return {
      subtitle,

      features,
    };
  },
};
</script>
