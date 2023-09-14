from classes.preferences    import Preferences
from classes.tools          import tag

class Tags:
    
    def getTags():
        return {
            'plugins'           : Tags.plugins,
            'no-welcome'        : Tags.no_welcome,
            'non-interactive'   : Tags.non_interactive,
            'reload'            : Tags.reload,
        }

    def replace( payload ):
        for k,v in Tags.getTags().items():
            payload = payload.replace(tag(k),v())
        return payload
    
    # TAG Translation callbacks below
    
    '@OBJECT'
    def plugins():
        from classes.plugin import Plugin
        return 'plugins: {'+",".join([f"{x}:undefined" for x in Plugin.loaded.keys() if Plugin.loaded[x].settings['enabled']])+"},"

    '@JSCRIPT'
    def no_welcome():
        return '''
            TO.dom.overlay.remove();
            TO.start();
        ''' if Preferences.settings['no-welcome'] else ''
    
    '@JSCRIPT:DEPRECATED'
    def reload():
        return "function refresh(){ window.location.reload(); } setInterval(refresh,5000);"

    '@CSSRULE'
    def non_interactive():
        return '* { pointer-events: none; }'


    
