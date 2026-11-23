using System.Collections.Generic;
using UnityEngine;

namespace BotAction
{
	public class BA_Nano_WatchOutTeammate : BotActionBase
	{
		private float nextChangeTime;

		private Transform teammate;

		private List<Collider> cldList;

		public BA_Nano_WatchOutTeammate(Bot bot)
			: base(null)
		{
		}

		private void Bot_Getter_ZoomDirection(ref Vector3 zoomDir, ref int priority)
		{
		}

		public override void Update()
		{
		}

		protected override void OnActionFinish()
		{
		}

		public override bool CanDo()
		{
			return false;
		}

		public override void DoAction()
		{
		}
	}
}
