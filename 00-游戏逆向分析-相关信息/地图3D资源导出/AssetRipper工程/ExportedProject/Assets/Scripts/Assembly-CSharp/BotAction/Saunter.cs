using Pathfinding;
using UnityEngine;

namespace BotAction
{
	public class Saunter : BotActionBase
	{
		private Vector3 targetPos;

		private bool pathOver;

		private float nanoEndTime;

		private float nextCheckTime;

		public bool isSaunter { get; private set; }

		public bool isReach { get; private set; }

		public bool isOccupyingPathfinder => false;

		public Saunter(Bot bot)
			: base(null)
		{
		}

		private void Bot_Destination_Listener(ref Vector3 pos, ref int priority)
		{
		}

		public override bool CanDo()
		{
			return false;
		}

		public override void DoAction()
		{
		}

		public void OnPathComplete(Path newPath)
		{
		}
	}
}
