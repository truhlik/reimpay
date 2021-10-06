export default function getMenuItems(vueInstance) {
  const isAdmin = vueInstance.$store.getters['account/isAdmin']

  let menu = [
    {
      header: true,
      title: vueInstance.$t('menu.title'),
    },
    {
      title: vueInstance.$t('menu.studies'),
      icon: 'pe-7s-note2',
      href: vueInstance.localePath({name: 'studies'}),
      child: [
        ...getStudyMenuList(vueInstance, isAdmin),
      ]
    },
  ]

  if (isAdmin) {
    // vueInstance not safe byt only for admin I want to add under studyMenuList option for new study
    menu[1].child.push(
      {
        title: `+ ${vueInstance.$t('common.newStudy')}`,
        href: vueInstance.localePath({name: 'studies-new-setup'}),
      },
    )

    menu.push(
      {
        title: vueInstance.$t('menu.company'),
        icon: 'pe-7s-home',
        href: vueInstance.localePath({name: 'company'})
      },
      {
        title: vueInstance.$t('menu.invoices'),
        icon: 'pe-7s-news-paper',
        href: vueInstance.localePath({name: 'company-invoices'})
      },
      {
        title: vueInstance.$t('menu.users'),
        icon: 'pe-7s-users',
        href: vueInstance.localePath({name: 'company-users'})
      },
    )
  }
  menu.push({
    title: vueInstance.$t('menu.contact'),
    icon: 'pe-7s-info',
    href: vueInstance.localePath({name: 'contact'})
  })


  return menu
}

function getStudyMenuList(vueInstance, isAdmin) {
  return vueInstance.studyList.map(s => ({
    title: s.identifier,
    href: vueInstance.localePath({name: isAdmin ? 'studies-id-setup' : 'studies-id-patients', params: {id: s.id}}),
    alias: [
      `/studies/${s.id}/setup/`,
      `/studies/${s.id}/general/`,
      `/studies/${s.id}/reims/`,
      `/studies/${s.id}/visits/`,
      `/studies/${s.id}/sites/`,
      `/studies/${s.id}/patients/`,
      `/studies/${s.id}/approvals/`,
      `/studies/${s.id}/finance/`,
      `/studies/${s.id}/stats/`,
      `/studies/${s.id}/history/`,
    ]
  }));
}
