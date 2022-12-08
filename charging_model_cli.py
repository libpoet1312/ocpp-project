import asyncio
import aioconsole
import logging
from datetime import datetime


try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys

    sys.exit(1)

from ocpp.routing import on
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as Base_ChargePoint
from ocpp.v16.enums import Action, RegistrationStatus, ChargingProfileStatus

logging.basicConfig(level=logging.INFO)


class ChargePoint(Base_ChargePoint):

    @on("SetChargingProfile")
    async def on_set_charging_profile(self, *args, **kwargs):
        return call_result.SetChargingProfilePayload(status="Accepted")

    @on(Action.DataTransfer)
    def on_datatransfer(self, **kwargs):
        return call_result.DataTransferPayload(
            status="Accepted",  # /"Rejected"/"UnknownMessageId"/"UnknownVendorId",
            data='string'
        )

    # cancelReservaon.conf(status)
    @on(Action.CancelReservation)
    def on_cancel_reservation(self, **kwargs):
        return call_result.CancelReservationPayload(
            status="Accepted"  # /"Rejected"
        )

    # changeAvailability.conf(status)
    @on(Action.ChangeAvailability)
    def on_change_availability(self, **kwargs):
        return call_result.ChangeAvailabilityPayload(
            status="Accepted"  # /"Rejected"/"Scheduled"
        )

    # changeconfiguration.conf(status)
    @on(Action.ChangeConfiguration)
    def on_change_configuration(self, **kwargs):
        return call_result.ChangeConfigurationPayload(
            status="Accepted"  # /"Rejected"/"RebootRequired"/ "NotSupported"
        )

    # clearcache.conf(status)
    @on(Action.ClearCache)
    def on_clear_cache(self, **kwargs):
        return call_result.ClearCachePayload(
            status="Accepted"  # /"Rejected"
        )

    # clearCache.conf(status)
    @on(Action.ClearChargingProfile)
    def on_clear_charging_profile(self, **kwargs):
        return call_result.ClearChargingProfilePayload(
            status="Accepted"  # /"Unknown"
        )

    # getcompositeschedule.conf(status,[connectorId],[scheduleStart],[chargingSchedule])
    @on(Action.GetCompositeSchedule)
    def on_get_composite_schedule(self, **kwargs):
        return call_result.GetCompositeSchedulePayload(
            status="Accepted",  # /"Rejected",
            connector_id=10,
            schedule_start='string'  # ,
            # charging_schedule={Dict}
        )

    # getconfiguration.conf(configurationKey,[unknownKey])
    @on(Action.GetConfiguration)
    def on_get_configuration(self, **kwargs):
        return call_result.GetConfigurationPayload(
            configuration_key=[{'key': "something"}],
            # unknownKey=[List]
        )

        # getDiagnostics.conf([fileName])

    @on(Action.GetDiagnostics)
    def on_get_diagnostics(self, **kwargs):
        return call_result.GetDiagnosticsPayload(
            file_name='string'
        )

    # GETlOCALlISTVersion.conf(listVersion)
    @on(Action.GetLocalListVersion)
    def on_get_local_list(self, **kwargs):
        return call_result.GetLocalListVersionPayload(
            list_version=10
        )

    # remoteStartTransaction.conf(status)
    @on(Action.RemoteStartTransaction)
    def on_get_remote_start_transaction(self, **kwargs):
        return call_result.RemoteStartTransactionPayload(
            status="Accepted"  # /"Rejected"
        )

    # remoteStopTransaction.conf(status)
    @on(Action.RemoteStartTransaction)
    def on_get_remote_stop_transaction(self, **kwargs):
        return call_result.RemoteStopTransactionPayload(
            status="Accepted"  # /"Rejected"
        )

    # reserveNow.conf(status)
    @on(Action.ReserveNow)
    def on_reserve_now(self, **kwargs):
        return call_result.ReserveNowPayload(
            status="Accepted"  # /"Faulted"/"Occupied"/"Rejected"/"Unavailable"
        )

    # reseet.conf(status)
    @on(Action.Reset)
    def on_reset(self, **kwargs):
        return call_result.ResetPayload(
            status="Accepted"  # /"Rejected"
        )

    # sendLocalList.conf(status)
    @on(Action.SendLocalList)
    def on_local_list(self, **kwargs):  # na to tsekarw
        return call_result.SendLocalListPayload(
            status="Accepted"  # /"Failed"/"NotSupported"/"VersionMismatch"
        )

    # triggerMessage.conf(status)
    @on(Action.TriggerMessage)
    def on_trigger(self, **kwargs):
        return call_result.TriggerMessagePayload(
            status="Accepted#" / "Rejected" / "NotImplemented"
        )

    # unlockConnector.conf(status)
    @on(Action.UnlockConnector)
    def on_trigger(self, **kwargs):
        return call_result.UnlockConnectorPayload(
            status="Unlocked" / "UnlockFailed" / "NotSupported"
        )

    # updateFirmware.conf()
    @on(Action.UpdateFirmware)
    def on_trigger(self, **kwargs):
        return call_result.UpdateFirmwarePayload()


async def send_authorize(cp):
    request = call.AuthorizePayload(
        id_tag="something"  # sunexeia apo edw
    )
    await cp.call(request)
    print("AUTHORIZE OK")


async def send_boot_notification(cp):
    request = call.BootNotificationPayload(
        charge_point_model="Optimus",
        charge_point_vendor="The Mobility House"
    )

    response = await cp.call(request)

    if response.status == RegistrationStatus.accepted:
        print("Connected to central system BOOT.")


async def start_transaction_notification(cp):
    request = call.StartTransactionPayload(
        connector_id=1,
        id_tag='1',
        meter_start=20,
        timestamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
    )

    response = await cp.call(request)

    if response.id_tag_info["status"] == 'Accepted':
        print("TRANSACTION")


async def stop_transaction_notification(cp):
    request = call.StopTransactionPayload(
        transaction_id=int(1),
        id_tag='1',
        timestamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z",
        meter_stop=30
    )
    response = await cp.call(request)

    if response.id_tag_info["status"] == 'Accepted':
        print("STOP TRANSACTION!!!!!")


async def send_meter_values(cp):
    time_meter = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"

    request = call.MeterValuesPayload(
        connector_id=1,
        meter_value=[{'timestamp': time_meter, 'sampledValue': [{'value': '200', 'measurand': 'Voltage', 'unit': 'V'}]},
                     {'timestamp': time_meter,
                      'sampledValue': [{'value': '100', 'measurand': 'SoC', 'unit': 'Percent'}]},
                     {'timestamp': time_meter,
                      'sampledValue': [{'value': '20', 'measurand': 'Energy.Active.Import.Register', 'unit': 'Wh'}]}],
        transaction_id=int(1)

    )

    await cp.call(request)
    print("METER")


'''
diagnosticStatusNotification.req(status)
diagnosticsStatusNotification.conf()
'''


async def send_diagnosticStatus(cp):
    request = call.DiagnosticsStatusNotificationPayload(
        status='Idle'  # /Uploaded/UploadFailed/Uploading'
    )
    await cp.call(request)
    print("DIAGNO OK ")


'''
firmwarestatusnotification.req(status)
firmwarestatusnotification.conf()
'''


async def send_firmwareStatus(cp):
    request = call.FirmwareStatusNotificationPayload(
        status="Downloaded"  # /"DownloadFailed"/ "Downloading""Idle"/"InstallationFailed"/"Installing"/"Installed"
    )
    await cp.call(request)
    print("FIRMWARE OK ")


'''
heartbeat.req()
heartbeat.conf(currentTime)
'''


async def send_heartbeat(cp):
    request = call.HeartbeatPayload()
    await cp.call(request)
    print("HEART OK ")


'''
datatrasfer.req(vendorId,[messageId],[data])
datatransfer.conf(status,[data])
'''


async def send_data_transfer(cp):
    request = call.DataTransferPayload(
        vendor_id='INVALID-VENDOR',  # Triggers a Rejected response
        message_id='string',
        data='string'
    )
    await cp.call(request)
    print("DATA OK ")


async def main():
    try:
        ws = websockets.connect(
            'ws://127.0.0.1:8000/123',  #
            subprotocols=['ocpp1.6'])
    except Exception as skata:
        print(skata)
        exit()
    else:
        cp = ChargePoint('CP_1', ws)
        console_task = asyncio.create_task(console(cp))

        await cp.start()

        await console_task


async def console(cp):
    try:
        logging.info("Started console")
        while True:
            line = await aioconsole.ainput('>')
            if 'help' in line:
                logging.info("TODO Create help menu")
            elif 'send-boot' in line:
                task = asyncio.create_task(send_boot_notification(cp))
                await task
            elif 'send-start' in line:
                task = asyncio.create_task(start_transaction_notification(cp))
                await task
            elif 'send-stop' in line:
                task = asyncio.create_task(stop_transaction_notification(cp))
                await task
            elif 'send-meter' in line:
                task = asyncio.create_task(send_meter_values(cp))
                await task
            elif 'send-authorize' in line:
                task = asyncio.create_task(send_authorize(cp))
                await task
            elif 'send-diagnostic' in line:
                task = asyncio.create_task(send_diagnosticStatus(cp))
                await task
            elif 'send-firmware' in line:
                task = asyncio.create_task(send_firmwareStatus(cp))
                await task
            elif 'send-heartbeat' in line:
                task = asyncio.create_task(send_heartbeat(cp))
                await task
            elif 'send-data' in line:
                task = asyncio.create_task(send_data_transfer(cp))
                await task

            else:
                logging.info("Unknown command: {}".format(line))
    except Exception as e:
        logging.error("Caught exception {}".format(e))


if __name__ == '__main__':
    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError as e:
        print(e)
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
