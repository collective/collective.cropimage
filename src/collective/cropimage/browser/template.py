from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cropimage import _
from collective.cropimage.id import ID
from collective.cropimage.interfaces import IAddID
from collective.cropimage.interfaces import IID
from persistent.dict import PersistentDict
from plone.app.z3cform.layout import wrap_form
from plone.registry.interfaces import IRegistry
from plone.z3cform.crud import crud
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility


class CropImageIDControlPanelForm(crud.CrudForm):
    """Form for ControlPanel."""

    add_schema = IAddID
    update_schema = IID

    label = _(u'Crop Image ID')

    def update(self):
        super(self.__class__, self).update()
        edit_forms = self.subforms[0]
        forms = edit_forms.subforms
        for form in forms:
            form.widgets['id'].size = 10
            form.widgets['ratio_width'].size = 3
            form.widgets['ratio_height'].size = 3
            form.widgets['min_width'].size = 3
            form.widgets['min_height'].size = 3
            form.widgets['max_width'].size = 3
            form.widgets['max_height'].size = 3
        add_form = self.subforms[1]
        add_form.widgets['id'].size = 10
        add_form.widgets['ratio_width'].size = 3
        add_form.widgets['ratio_height'].size = 3
        add_form.widgets['min_width'].size = 3
        add_form.widgets['min_height'].size = 3
        add_form.widgets['max_width'].size = 3
        add_form.widgets['max_height'].size = 3

    def add(self, data):
        """Add new ID data to collective.cropimage.ids registry.

        :param data: ID data.
        :type data: dict
        """
        registry = getUtility(IRegistry)
        items = registry['collective.cropimage.ids']
        items[data.pop(u'id')] = data
        registry['collective.cropimage.ids'] = items

    def get_items(self):
        """Get items to show on the form."""
        registry = getUtility(IRegistry)
        items = registry['collective.cropimage.ids']
        data = []
        for key in items:
            data.append((key, ID(key, **items[key])))
        return data

    def remove(self, (id, item)):
        """Delete ID data from collective.cropimage.ids registry.

        :param id: Unique ID name.
        :type id: str

        :param item: collective.cropimage.id.ID instance.
        :type id: object
        """
        registry = getUtility(IRegistry)
        items = registry['collective.cropimage.ids']
        del items[id]
        registry['collective.cropimage.ids'] = items

    def before_update(self, item, data):
        registry = getUtility(IRegistry)
        items = registry['collective.cropimage.ids']
        items[item.id] = data
        registry['collective.cropimage.ids'] = items

CropImageIDControlPanelView = wrap_form(
    CropImageIDControlPanelForm,
    index=ViewPageTemplateFile('templates/controlpanel.pt'))


class CropImageView(BrowserView):

    template = ViewPageTemplateFile('templates/crop_image.pt')

    def __call__(self):
        context = aq_inner(self.context)
        form = self.request.form
        if form.get('form.button.Save', None) is not None:
            name = 'collective.cropimage.{0}'.format(
                form.get('field')
            )
            anno = IAnnotations(context)
            if anno.get(name) is None:
                anno[name] = PersistentDict()
            anno[name].update(self.dimension(form))
        return self.template()

    @property
    def ids(self):
        registry = getUtility(IRegistry)
        return registry['collective.cropimage.ids']

    @property
    def selected_id(self):
        return self.request.form.get('id-name') or self.ids.keys()[0]

    def select(self):
        """Form select tag with the ID options."""
        name = 'id-name'
        html = '<select name="{0}" id="{0}">'.format(name)
        for key in self.ids:
            if key == self.selected_id:
                html += '<option value="{0}" selected="selected">{0}</option>'.format(key)
            else:
                html += '<option value="{0}">{0}</option>'.format(key)
        html += '</select>'
        return html

    def script(self):
        data = self.ids[self.selected_id]
        ratio_width = data['ratio_width']
        ratio_height = data['ratio_height']
        min_width = data['min_width']
        min_height = data['min_height']
        max_width = data['max_width']
        max_height = data['max_height']
        aspectRatio = 'aspectRatio: {0}/{1},'.format(ratio_width, ratio_height) if (
            ratio_width != 0.0
        ) and (
            ratio_height != 0.0
        ) else None
        minSize = 'minSize: [{0}, {1}],'.format(min_width, min_height) if (
            min_width != 0.0
        ) and (
            min_height != 0.0
        ) else None
        maxSize = 'maxSize: [{0}, {1}],'.format(max_width, max_height) if (
            max_width != 0.0
        ) and (
            max_height != 0.0
        ) else None
        variables = ''
        variables += aspectRatio if aspectRatio is not None else ''
        variables += minSize if minSize is not None else ''
        variables += maxSize if maxSize is not None else ''
        script = """<script type="text/javascript">
        // Remember to invoke within jQuery(window).load(...)
        // If you don't, Jcrop may not initialize properly
        $(function(){
            $('#jcrop_target').Jcrop({
                onChange: showCoords,
                onSelect: showCoords,"""
        script += variables
        script += """
            });
        });

        // Our simple event handler, called from onChange and onSelect
        // event handlers, as per the Jcrop invocation above
        function showCoords(c)
        {
            $('#x').val(c.x);
            $('#y').val(c.y);
            $('#x2').val(c.x2);
            $('#y2').val(c.y2);
            $('#w').val(c.w);
            $('#h').val(c.h);
        };
</script>
"""
        return script

    def fields(self):
        """Returns list of field names."""
        context = aq_inner(self.context)
        return context.restrictedTraverse("image-fields")()

    def dimension(self, form):
        """Returns dictionary with ID name as key and dimension values as value.

        :param form: Form data
        :type form: dict
        """
        keys = ['x', 'x2', 'y', 'y2', 'w', 'h']
        res = {}
        for key in keys:
            res.update(
                {key: form[key]}
            )
        return {form.get('id-name'): res}

    def images(self):
        """Image related values for each fields."""
        context = aq_inner(self.context)
        results = []
        for field in self.fields():
            full = context.getField(field).tag(context)
            item = {
                'full-image': '{0} id="jcrop_target" {1}'.format(full[:4], full[5:]),
                'select': self.select(),
                'field': field,
                'previews': self.previews(field),
            }
            results.append(item)
        return results

    def current_url(self):
        """Current URL."""
        context_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_context_state'
        )
        return context_state.current_page_url()

    def previews(self, field):
        """Previews for field.

        :param field: Field name.
        :type field: str
        """
        context = aq_inner(self.context)
        anno = IAnnotations(context)
        name = 'collective.cropimage.{0}'.format(field)
        prev = anno.get(name)
        if prev is not None:
            prevs = []
            for key in prev.keys():
                html = '<article class="preview" id="{0}-{1}-preview">'.format(field, key)
                html += '<h1>{0}</h1>'.format(key)
                html += context.restrictedTraverse('cropped-image')(field, key)
                html += '</article>'
                prevs.append(html)
            return prevs
