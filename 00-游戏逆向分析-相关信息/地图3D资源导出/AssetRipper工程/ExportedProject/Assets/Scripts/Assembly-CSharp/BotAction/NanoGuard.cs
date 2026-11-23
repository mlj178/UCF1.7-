using UnityEngine;

namespace BotAction
{
	public class NanoGuard
	{
		private Bot bot;

		private float nextChangePosTime;

		private Vector3 escapePos;

		public bool isArriveArea { get; private set; }

		public bool isArrivePos { get; private set; }

		public Bot_NanoGuardArea guardArea { get; private set; }

		public Bot_NanoGuardPos guardPos { get; private set; }

		public bool isGoingGuardPos => false;

		private NanoRole nanoRole => NanoRole.Soldier;

		public bool isEscaping { get; private set; }

		public NanoGuard(Bot bot)
		{
		}

		private void Bot_Getter_ZoomDirection(ref Vector3 zoomDir, ref int priority)
		{
		}

		private void Bot_Destination_Listener(ref Vector3 pos, ref int priority)
		{
		}

		public void Update()
		{
		}

		public void Clear()
		{
		}

		private void UpdateArea()
		{
		}

		private void RandomChangeGuardPos()
		{
		}

		private void GoToSaferGuardPos()
		{
		}

		public void OnEnterArea()
		{
		}

		public void SetAreaTarget(Bot_NanoGuardArea targetArea)
		{
		}

		public void OnExitArea()
		{
		}

		private void SetGuardPos(Bot_NanoGuardPos newPos)
		{
		}
	}
}
