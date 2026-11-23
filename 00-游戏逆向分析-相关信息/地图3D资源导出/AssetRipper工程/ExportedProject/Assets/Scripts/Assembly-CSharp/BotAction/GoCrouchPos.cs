using UnityEngine;

namespace BotAction
{
	public class GoCrouchPos : BotActionBase
	{
		private Bot_CrouchPos target;

		private float giveUpTime;

		public GoCrouchPos(Bot bot)
			: base(null)
		{
		}

		private void Bot_Getter_ZoomDirection(ref Vector3 zoomDir, ref int priority)
		{
		}

		private void Bot_Destination_Listener(ref Vector3 pos, ref int priority)
		{
		}

		public override void Update()
		{
		}

		public override bool CanDo()
		{
			return false;
		}

		public override void DoAction()
		{
		}

		protected override void OnActionFinish()
		{
		}

		private void GiveUp()
		{
		}
	}
}
