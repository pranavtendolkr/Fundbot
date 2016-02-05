from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

import subprocess as sub
import tradeoff
import dialog
import grapher

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        # send receipt otherwise we keep receiving the same message over and over

        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
            message=messageProtocolEntity.getBody()
            print message + "\n"

            output,client_id = dialog.converse( messageProtocolEntity.getFrom(),message)

            if output == "Okay, thank you for using the service!":
                profile = dialog.get_profile(client_id)
                response,profile_has_graph = tradeoff.call_tradeoff_api(profile)
                print type(response)
                if(profile_has_graph is True):
                    link = grapher.PlotGraphi.plot_graph(str(response))
                top5 = grapher.PlotGraph.top_five(response)
                output = "The top mutual funds we selected for you are:\n"
                for i,item in enumerate(top5):
                    output = output + '%i,%s\n'%(i,item)
                output = output + "\n and here is the graph you requested \n %s"%(link)

            print output
            #output=message
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(output,
                to = messageProtocolEntity.getFrom())

            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
